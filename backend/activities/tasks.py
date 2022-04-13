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
        activity_type=Activity.WORK
    )[:1]

    for activity in activities:
        with transaction.atomic():
            activity = Activity.objects.select_for_update().get(
                pk=activity.pk,
                activity_type=Activity.WORK
            )

            smartcontract.work(
                activity.user.account.address,
                activity.user.account.private_key,
                activity.id,
                activity.reward,
                activity.project.app_id
            )

            if (activity.task.finished
                or (activity.project.usdc_balance() < activity.reward)
            ):
                activity.status = Activity.REJECTED
                activity.sync = Activity.TO_SYNC
            else:
                activity.sync = Activity.SYNCED

            activity.save()


@shared_task()
def verify_activity():
    activities = Activity.objects.filter(
        sync=Activity.TO_SYNC,
        activity_type=Activity.WORK
    )[:1]

    for activity in activities:
        with transaction.atomic():
            activity = Activity.objects.select_for_update().get(
                pk=activity.pk,
                activity_type=Activity.WORK
            )

            if ((activity.status == Activity.ACCEPTED and activity.task.finished)
                or (activity.project.usdc_balance() < activity.reward)
            ):
                activity.status = Activity.REJECTED

            smartcontract.verify(
                activity.project.owner.account.address,
                activity.project.owner.account.private_key,
                activity.user.account.address,
                activity.id,
                activity.reward,
                activity.status,
                activity.project.app_id
            )
            activity.sync = Activity.SYNCED
            activity.save()
            
            accepted_activity_count = Activity.objects.filter(
                task=activity.task,
                activity_type=Activity.WORK, 
                status=Activity.ACCEPTED
            ).count()
        
        with transaction.atomic():
            task = Task.objects.select_for_update().get(id=activity.task.id)
            if accepted_activity_count >= task.count:
                Task.objects.filter(
                    pk=task.pk
                ).update(
                    finished=True
                )
