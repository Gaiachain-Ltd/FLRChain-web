import datetime
from celery import shared_task
from investments.models import Investment
from django.db.models import F
from algorand.smartcontract import invest

@shared_task()
def project_invest():
    investments = Investment.objects.filter(
        status=Investment.INITIAL
    )

    for investment in investments:
        invest(
            investment.investor.account.address,
            investment.investor.account.private_key,
            investment.project.app_id,
            investment.amount
        )
        investment.sync = Investment.SYNCED
        investment.save()