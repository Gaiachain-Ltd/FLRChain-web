import logging
import datetime
import base64
from projects.models import *
from accounts.models import Account
from users.models import CustomUser
from celery import shared_task
from algorand import smartcontract
from algorand.utils import *
from django.conf import settings
from django.db.models import F, Sum, Q, Count
from django.db import transaction
from activities.models import Activity


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
            project.app_id,
            int(
                datetime.datetime.combine(
                    project.start,
                    datetime.time(0, 0, 0, 0)
                ).timestamp()
            ),
            int(
                datetime.datetime.combine(
                    project.end,
                    datetime.time(0, 0, 0, 0)
                ).timestamp()
            ),
            project.fac_adm_funds,
            project.status
        )
        project.state = Project.INITIALIZED
        project.sync = Project.SYNCED
        project.save()


@shared_task()
def start_project():
    projects = Project.objects.filter(
        state=Project.INITIALIZED,
        status=Project.FUNDRAISING,
        sync=Project.SYNCED,
        start__lte=datetime.datetime.now().date()
    ).annotate(reward_total=Sum(
        F('task__reward') * F('task__count')
    )).annotate(batch_total=Sum('task__batch')).annotate(
        total=F('fac_adm_funds') + F('reward_total') + F('batch_total')
    )

    for project in projects:
        print("USDC: ", usdc_balance(application_address(project.app_id)), project.total)
        if usdc_balance(application_address(project.app_id)) < project.total:
            project.state = Project.POSTPONED
        else:
            project.state = Project.STARTED
            project.status = Project.ACTIVE
            project.sync = Project.TO_SYNC
        project.save()


@shared_task()
def update_project():
    projects = Project.objects.select_for_update().filter(
        Q(sync=Project.TO_SYNC) &
        ~Q(state__in=[Project.INITIAL, Project.CREATED, Project.DELETED])
    ).order_by('-modified')

    with transaction.atomic():
        for project in projects:
            smartcontract.update(
                project.owner.account.address,
                project.owner.account.private_key,
                project.app_id,
                int(
                    datetime.datetime.combine(
                        project.start,
                        datetime.time(0, 0, 0, 0)
                    ).timestamp()
                ),
                int(
                    datetime.datetime.combine(
                        project.end,
                        datetime.time(0, 0, 0, 0)
                    ).timestamp()
                ),
                project.fac_adm_funds,
                project.status
            )
            project.sync = Project.SYNCED
            project.save()


@shared_task()
def finish_project():
    projects = Project.objects.select_for_update().filter(
        state=Project.STARTED,
        status=Project.ACTIVE,
        end__lte=datetime.datetime.now().date()
    )

    with transaction.atomic():
        for project in projects:
            project.status = Project.CLOSED
            project.state = Project.FINISHED
            project.sync = Project.TO_SYNC
            project.save()


@shared_task()
def close_project():
    projects = Project.objects.filter(
        state=Project.FINISHED,
        status=Project.CLOSED
    )

    for project in projects:
        investors_data = INDEXER.accounts(
            application_id=project.app_id)['accounts']
        investor_address_list = defaultdict(list)
        for investor_data in investors_data:
            apps_local_state = investor_data['apps-local-state']
            for app_local_state in apps_local_state:
                if app_local_state['id'] == project.app_id:
                    for key_value in app_local_state['key-value']:
                        if base64.b64decode(key_value['key']).decode() == "role":
                            investor_address_list[key_value['value']['uint']].append(
                                investor_data['address'])

        addresses = list()
        for role in sorted(investor_address_list.keys(), reverse=True):
            addresses.extend(investor_address_list[role])

        keys = list()
        txns = list()
        for address in addresses:
            account = Account.objects.get(address=address)
            txns.append(smartcontract.opt_out(account.address, project.app_id))
            keys.append(account.private_key)

            if len(txns) == 15:
                txn = sign_send_atomic_trasfer(keys, txns)
                wait_for_confirmation(txn)

                keys = list()
                txns = list()

        if len(txns) > 12:
            txn = sign_send_atomic_trasfer(keys, txns)
            wait_for_confirmation(txn)
            keys = list()
            txns = list()

        main = Account.get_main_account()
        account = project.account

        txns.append(
            smartcontract.delete_application(account.address, project.app_id)
        )
        keys.append(account.private_key)

        txn2, _ = prepare_transfer_assets(
            account.address,
            main.address,
            0,
            close_assets_to=main.address
        )
        txns.append(txn2)
        keys.append(account.private_key)

        txn3, _ = prepare_transfer_algos(
            account.address,
            main.address,
            0,
            close_remainder_to=main.address
        )
        txns.append(txn3)
        keys.append(account.private_key)

        txn = sign_send_atomic_trasfer(keys, txns)
        wait_for_confirmation(txn)

        project.state = Project.DELETED
        project.status = Project.CLOSED
        project.sync = Project.SYNCED
        project.save()


@shared_task()
def join_project():
    assignments = Assignment.objects.filter(
        sync=Assignment.INITIAL
    )

    for assignment in assignments:
        account = assignment.beneficiary.account
        smartcontract.join(
            account.address,
            account.private_key,
            assignment.project.app_id
        )
        assignment.sync = Assignment.SYNCED
        assignment.save()


@shared_task()
def beneficiary_approval():
    assignments = Assignment.objects.filter(
        sync=Assignment.TO_SYNC
    )

    for assignment in assignments:
        account = assignment.beneficiary.account
        smartcontract.approval(
            assignment.project.owner.account.address,
            assignment.project.owner.account.private_key,
            account.address,
            Assignment.ACCEPTED if assignment.status == Assignment.ACCEPTED else Assignment.REJECTED,
            assignment.project.app_id
        )
        assignment.sync = Assignment.SYNCED
        assignment.save()


@shared_task()
def payout_batch():
    tasks = Task.objects.filter(
        activity__status=Activity.ACCEPTED,
        project__status=Project.ACTIVE,
        batch_paid=False,
        finished=True,
        batch__gte=0
    )
    for task in tasks:
        beneficiaries = Assignment.objects.filter(
            project=task.project,
            status=Assignment.ACCEPTED
        )

        amount = task.batch / beneficiaries.count()
        
        txns = list()
        for beneficiary in beneficiaries:
            batch_activity = Activity.objects.create(
                user=beneficiary.beneficiary,
                task=task,
                project=task.project,
                reward=amount,
                activity_type=Activity.BATCH,
                sync=Activity.TO_SYNC,
                status=Activity.ACCEPTED
            )

            txns.append(
                smartcontract.batch(
                    task.project.owner.account.address,
                    beneficiary.beneficiary.account.address,
                    batch_activity.id,
                    int(amount * 1000000),
                    task.project.app_id
                )
            )

            if len(txns) == 15:
                txn = sign_send_atomic_trasfer(
                    task.project.owner.account.private_key,
                    txns
                )
                wait_for_confirmation(txn)
                txns = list()

        txn = sign_send_atomic_trasfer(
            task.project.owner.account.private_key,
            txns
        )
        wait_for_confirmation(txn)

        Activity.objects.filter(
            task=task, 
            activity_type=Activity.BATCH, 
            sync=Activity.TO_SYNC
        ).update(
            sync=Activity.SYNCED
        )
        
        task.batch_paid = True
        task.save()