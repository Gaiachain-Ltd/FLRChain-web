import logging
from algorand import smartcontract
from celery import shared_task
from activities.models import Activity


logger = logging.getLogger(__name__)


@shared_task()
def create_activity():
    activities = Activity.objects.filter(
        state=Activity.INITIAL,
    )

    for activity in activities:
        smartcontract.work(
            activity.user.account.address,
            activity.user.account.private_key,
            activity.id,
            int(activity.task.reward * 1000000),
            activity.project.app_id
        )
        activity.state = Activity.SYNCED
        activity.save()


@shared_task()
def verify_activity():
    activities = Activity.objects.filter(
        state=Activity.TO_SYNC
    )

    for activity in activities:
        smartcontract.verify(
            activity.project.owner.account.address,
            activity.project.owner.account.private_key,
            activity.user.account.address,
            activity.id,
            int(activity.reward * 1000000),
            activity.status,
            activity.project.app_id
        )
        activity.state = Activity.SYNCED
        activity.save()
