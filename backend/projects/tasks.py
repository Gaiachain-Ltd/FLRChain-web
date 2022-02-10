import logging
from projects.models import Project
from accounts.models import Account
from celery import shared_task
from algorand import smartcontract
from django.conf import settings


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
            project.app_id
        )
        project.state = Project.INITIALIZED
        project.save()
        
@shared_task()
def start_project():
    projects = Project.objects.filter(
        state=Project.INITIALIZED, 
        status=Project.FUNDRAISING
    )
    