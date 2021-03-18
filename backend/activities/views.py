from django.shortcuts import render
from common.views import CommonView
from activities.serializers import ActivitySerializer
from drf_yasg.utils import swagger_auto_schema


class ActivityView(CommonView):
    serializer_class = ActivitySerializer

    @swagger_auto_schema(
        operation_summary="Create new activity",
        request_body=ActivitySerializer,
        tags=['activities', 'beneficiary'])
    def create(self, request, project_pk=None, task_pk=None):
        pass