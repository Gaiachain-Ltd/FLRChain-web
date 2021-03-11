from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from common.views import CommonView
from projects.models import Project
from projects.serializers import ProjectSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class ProjectView(CommonView):
    serializer_class = ProjectSerializer

    def get(self, request):
        projects = Project.objects.filter(owner=request.user)
        return self.paginated_response(projects, request)

    @swagger_auto_schema(
        operation_summary="Create new project",
        request_body=ProjectSerializer,
        tags=['projects'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={
            'owner': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)