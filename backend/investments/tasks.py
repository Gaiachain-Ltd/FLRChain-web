import datetime
from celery import shared_task
from investments.models import Investment
from django.db.models import F

@shared_task()
def finish_investment():
    finished_investments = Investment.objects.filter(
        status=Investment.INVESTED,
        end__lte=F('end') + datetime.timedelta(days=1))[:10]
    
    for finished_investment in finished_investments:
        finished_investment.finish()