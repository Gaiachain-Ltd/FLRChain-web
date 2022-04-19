import datetime
from celery import shared_task
from investments.models import Investment
from django.db.models import F
from algorand.smartcontract import invest


@shared_task()
def project_invest():
    investments = Investment.objects.filter(
        sync=Investment.TO_SYNC
    )[:1]

    for investment in investments:
        invest(
            investment.investor.account.address,
            investment.investor.account.private_key,
            investment.project.app_id,
            investment.amount,
            include_opt_in=not Investment.objects.filter(
                sync=Investment.SYNCED, 
                project=investment.project
            ).exists()
        )
        investment.sync = Investment.SYNCED
        investment.save()
