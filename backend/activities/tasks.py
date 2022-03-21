import logging
from algorand import smartcontract
from celery import shared_task
from activities.models import Activity
from django.db import transaction
from projects.models import Task


logger = logging.getLogger(__name__)


@shared_task()
def create_activity():
    activities = Activity.objects.filter(
        sync=Activity.INITIAL,
    )

    for activity in activities:
        smartcontract.work(
            activity.user.account.address,
            activity.user.account.private_key,
            activity.id,
            int(activity.task.reward * 1000000),
            activity.project.app_id
        )
        activity.sync = Activity.SYNCED
        activity.save()


@shared_task()
def verify_activity():
    activities = Activity.objects.filter(
        sync=Activity.TO_SYNC
    )

    for activity in activities:
        with transaction.atomic():
            # TODO: optimization
            activity = Activity.objects.select_for_update().get(pk=activity.pk)
            smartcontract.verify(
                activity.project.owner.account.address,
                activity.project.owner.account.private_key,
                activity.user.account.address,
                activity.id,
                int(activity.reward * 1000000),
                activity.status,
                activity.project.app_id
            )
            activity.sync = Activity.SYNCED
            activity.save()
            
            accepted_activity_count = Activity.objects.filter(
                task=activity.task, 
                status=Activity.ACCEPTED).count()
            task = Task.objects.get(id=activity.task.id)

            if accepted_activity_count == task.count:
                task.finished = True
                task.save()
