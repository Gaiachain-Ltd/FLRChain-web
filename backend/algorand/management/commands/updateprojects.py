from django.core.management.base import BaseCommand
from projects.models import Project
from accounts.models import Account
from algorand.smartcontract import update_contract

class Command(BaseCommand):
    def handle(self, *args, **options):
        for project in Project.objects.filter(
            status__in=[Project.ACTIVE, Project.FUNDRAISING],
            state__gte=Project.INITIALIZED
        ):
            project_account = Account.objects.get(project=project)
            update_contract(
                project_account.address,
                project_account.private_key,
                project.app_id
            )

