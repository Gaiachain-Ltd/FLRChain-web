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
from users.permissions import isBeneficiary


class ActivityView(CommonView):
    serializer_class = ActivitySerializer
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        """
        Only facililator can make and update projects.
        """
        if self.request.method == "POST":
            return [permission() for permission in [*self.permission_classes, isBeneficiary]]
        return [permission() for permission in self.permission_classes]


    @swagger_auto_schema(
        operation_summary="History activity",
        tags=['activities', 'beneficiary', 'investor', 'facililator'])
    def list(self, request, pk=None):
        if request.user.type == CustomUser.BENEFICIARY:
            activities = Activity.objects.filter(project=pk, user=request.user)
        else:
            activities = Activity.objects.filter(project=pk)
        return self.paginated_response(activities, request)

    @swagger_auto_schema(
        operation_summary="Create new activity",
        request_body=ActivitySerializer,
        tags=['activities', 'beneficiary'])
    def create(self, request, project_pk=None, task_pk=None):
        with transaction.atomic():
            project = get_object_or_404(
                Project.objects.with_beneficiary_assignment_status(request.user),
                assignment_status=Assignment.ACCEPTED,
                pk=project_pk)
                
            task = get_object_or_404(
                Task, 
                project=project, 
                pk=task_pk)

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            activity = serializer.save(
                user=request.user,
                project=project,
                task=task)

            transfer = Transaction.transfer(
                project.smartcontract.account,
                request.user.account,
                task.reward,
                Transaction.USDC,
                Transaction.REWARD,
                project=project)

            activity.transaction = transfer
            activity.save()

            serializer = self.serializer_class(activity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)