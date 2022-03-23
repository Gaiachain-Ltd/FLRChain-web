import base64
from django.shortcuts import get_object_or_404
from common.views import CommonView
from activities.serializers import ActivitySerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from projects.models import Assignment, Task, Project
from rest_framework import status
from rest_framework.response import Response
from activities.models import Activity
from django.db import transaction
from transactions.models import Transaction
from users.models import CustomUser
from users.permissions import isBeneficiary, isOptedIn
from algorand import utils
from algorand import smartcontract
from activities.serializers import *
from decimal import *


class ActivityView(CommonView):
    serializer_class = ActivitySerializer
    # parser_classes = (MultiPartParser,)

    # def get_permissions(self):
    #     """
    #     Only facililator can make and update projects.
    #     """
    #     if self.request.method == "POST":
    #         return [permission() for permission in [
    #             *self.permission_classes, isBeneficiary, isOptedIn]]
    #     return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(
        operation_summary="History activity",
        tags=['activities', 'investor', 'facililator'])
    def list(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        transactions = utils.get_transactions(
            application_id=project.app_id,
            note_prefix="W|".encode()
        )['transactions']

        status_filter = request.GET.get("status", None)
        
        data = dict()
        batches = dict()
        for transaction in transactions:
            notes = base64.b64decode(transaction['note']).decode().split('|')
            if len(notes) != 3:
                continue

            amount = base64.b64decode(transaction['application-transaction']['application-args'][1])
            activity_status = notes[1]
            if activity_status == "W":
                activity_status = Activity.WAITING
            elif activity_status == "V":
                value = base64.b64decode(transaction['application-transaction']['application-args'][2])
                activity_status = int.from_bytes(value, "big")
            elif activity_status == "B" and status_filter is None:
                activity_status = Activity.ACCEPTED
            else:
                continue

            if status_filter is not None and int(status_filter) != activity_status:
                continue

            activity_id = notes[2]
            data[activity_id] = {
                "id": activity_id,
                "txid": transaction['id'],
                "amount": int.from_bytes(amount, "big"),
                "status": activity_status,
                "round-time": transaction['round-time']
            }
        
        activities = Activity.objects.filter(id__in=data.keys())
        for activity in activities:
            data[str(activity.id)].update({
                "name": f"{activity.user.first_name} {activity.user.last_name}",
                "task_id": activity.task.id,
                "task_name": activity.task.name,
                "status": activity.status,
                "sync": activity.sync,
                "photos": activity.photos.count(),
                "text": activity.text,
                "area": activity.area,
                "number": activity.number,
                "activity_type": activity.activity_type
            })
        
        return Response(data.values(), status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create new activity",
        request_body=CreateActivitySerializer,
        responses={
            status.HTTP_201_CREATED: ActivitySerializer
        },
        tags=['activities', 'beneficiary'])
    def create(self, request, project_pk=None, task_pk=None):
        with transaction.atomic():
            project = get_object_or_404(
                Project.objects.with_beneficiary_assignment_status(request.user),
                assignment_status=Assignment.ACCEPTED,
                pk=project_pk
            )

            task = get_object_or_404(
                Task, 
                project=project, 
                pk=task_pk
            )

            serializer = CreateActivitySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            activity = serializer.save(
                user=request.user,
                project=project,
                task=task
            )

            serializer = self.serializer_class(activity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, project_pk=None, activity_pk=None):
        serializer = ActivityVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            project = get_object_or_404(
                Project, 
                pk=project_pk, 
                owner=request.user
            )
            activity = get_object_or_404(
                Activity.objects.select_for_update(), 
                pk=activity_pk,
                project=project
            )
            
            activity.status = serializer.validated_data['status']
            activity.sync = Activity.TO_SYNC
            activity.save()

        return Response(status=status.HTTP_200_OK)

    def distributed(self, request, project_pk=None):
        project = get_object_or_404(Project, pk=project_pk)
        transactions = utils.get_transactions(
            application_id=project.app_id,
            note_prefix="W|".encode()
        )['transactions']

        sum = 0
        for transaction in transactions:
            notes = base64.b64decode(transaction['note']).decode().split('|')
            if len(notes) != 3:
                continue

            if notes[1] not in ["V", "B"]:
                continue

            amount = base64.b64decode(transaction['application-transaction']['application-args'][1])
            sum += int.from_bytes(amount, "big")

        return Response({"sum": sum}, status=status.HTTP_200_OK)


class PhotoView(CommonView):
    serializer_class = ActivityPhotoSerializer
    parser_classes = (MultiPartParser,)

    def list(self, _, activity_pk=None):
        activity = get_object_or_404(
            Activity,
            pk=activity_pk
        )
        serializer = ActivityPhotoSerializer(activity.photos.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Add photo to activity",
        request_body=ActivityPhotoSerializer,
        responses={
            status.HTTP_201_CREATED: ActivitySerializer
        },
        tags=['activities', 'beneficiary']
    )
    def create(self, request, activity_pk=None):
        with transaction.atomic():
            activity = get_object_or_404(
                Activity.objects.select_for_update(),
                pk=activity_pk
            )

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            photo = serializer.save()
            activity.photos.add(photo)
            
            return Response(
                ActivitySerializer(activity), 
                status=status.HTTP_201_CREATED
            )