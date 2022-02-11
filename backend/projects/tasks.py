import logging
import datetime
import base64
from projects.models import Project
from accounts.models import Account
from users.models import CustomUser
from celery import shared_task
from algorand import smartcontract
from algorand.utils import usdc_balance, application_address, INDEXER, sign_send_atomic_trasfer, wait_for_confirmation
from django.conf import settings
from django.db.models import F, Sum


logger = logging.getLogger(__name__)


@shared_task()
def create_project():
    projects = Project.objects.filter(
        state=Project.INITIAL, 
        status=Project.FUNDRAISING
    )

    for project in projects:
        if not hasattr(project, "account"):
            account = Account.generate(
                project, 
                Account.PROJECT_ACCOUNT,
                settings.ALGO_APP_CREATE_AMOUNT,
                sync=True
            )
        account = project.account

        app_id = smartcontract.create(account.address, account.private_key)
        project.app_id = app_id
        project.state = Project.CREATED
        project.save()


@shared_task()
def initialize_project():
    projects = Project.objects.filter(
        state=Project.CREATED, 
        status=Project.FUNDRAISING
    )

    for project in projects:
        smartcontract.initialize(
            project.account.address, 
            project.account.private_key,
            project.owner.account.address,
            project.owner.account.private_key,
            project.app_id
        )
        project.state = Project.INITIALIZED
        project.save()
        
@shared_task()
def start_project():
    projects = Project.objects.filter(
        state=Project.INITIALIZED, 
        status=Project.FUNDRAISING,
        start__lte=datetime.datetime.now().date()
    ).annotate(reward_total=Sum(
        F('task__reward') * F('task__count')
    )).annotate(batch_total=Sum('task__batch')).annotate(
       total = F('fac_adm_funds') + F('reward_total') + F('batch_total')
    )

    for project in projects:
        if usdc_balance(application_address(project.app_id)) < project.total:
            project.state = Project.POSTPONED
            project.save()
        else:
            smartcontract.start(
                project.account.address,
                project.account.private_key,
                project.app_id,
                int(
                    datetime.datetime.combine(
                        project.start, 
                        datetime.time(0,0,0,0)
                    ).timestamp()
                ),
                int(
                    datetime.datetime.combine(
                        project.end, 
                        datetime.time(0,0,0,0)
                    ).timestamp()
                ),
                project.fac_adm_funds
            )
            project.state = Project.STARTED
            project.status = Project.ACTIVE
            project.save()


@shared_task()
def finish_project():
    projects = Project.objects.filter(
        state=Project.STARTED, 
        status=Project.ACTIVE,
        end__lte=datetime.datetime.now().date()
    )

    for project in projects:
        investors_data = INDEXER.accounts(application_id=project.app_id)['accounts']
        investor_address_list = list()
        for investor_data in investors_data:
            apps_local_state = investor_data['apps-local-state']
            for app_local_state in apps_local_state:
                if app_local_state['id'] == project.app_id:
                        for key_value in app_local_state['key-value']:
                            if base64.b64decode(key_value['key']).decode() == "role":
                                if key_value['value']['uint'] in [CustomUser.INVESTOR]:
                                    investor_address_list.append(investor_data['address'])
        keys = list()
        txns = list()
        for ial in investor_address_list:
            account = Account.objects.get(address=ial)
            txns.append(smartcontract.withdraw(account.address, project.app_id))
            keys.append(account.private_key)

            txns.append(smartcontract.opt_out(account.address, project.app_id))
            keys.append(account.private_key)

            if len(txns) == 15:
                txn = sign_send_atomic_trasfer(keys, txns)
                wait_for_confirmation(txn)

                keys = list()
                txns = list()

        if len(txns) > 0:
            txn = sign_send_atomic_trasfer(keys, txns)
            wait_for_confirmation(txn)
    
        project.state = Project.FINISHED
        project.status = Project.CLOSED
        project.save()
