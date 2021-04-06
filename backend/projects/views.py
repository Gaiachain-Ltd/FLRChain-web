from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from common.views import CommonView
from projects.models import Project, Assignment
from projects.serializers import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from users.models import CustomUser
from django_filters import rest_framework as filters


class ProjectView(CommonView):
    serializer_class = ProjectSerializer
    filterset_fields = {
        'investment': ['isnull',]
    }

    @swagger_auto_schema(
        operation_summary="Full project list",
        tags=['projects', 'facililator', 'beneficiary', 'investor'])
    def list(self, request):
        if request.user.type == CustomUser.BENEFICIARY:
            projects = Project.objects.with_beneficiary_assignment_status(
                request.user)
        elif request.user.type == CustomUser.FACILITATOR:
            projects = Project.objects.filter(owner=request.user)
        else:
            projects = Project.objects.for_investor(request.user)

        return self.paginated_response(projects, request)

    @swagger_auto_schema(
        operation_summary="Create new project",
        request_body=ProjectSerializer,
        tags=['projects', 'facililator'])
    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={
            'owner': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Project details",
        tags=['projects', 'facililator', 'beneficiary', 'investor'])
    def retrieve(self, request, pk=None):
        if request.user.type == CustomUser.BENEFICIARY:
            project = Project.objects.with_beneficiary_assignment_status(
                request.user).filter(pk=pk).first()
        else:
            project = Project.objects.filter(pk=pk).first()

        if not project:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Project update",
        tags=['projects', 'facililator'])
    def update(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        serializer = self.serializer_class(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignmentView(CommonView):
    serializer_class = AssignmentSerializer

    @swagger_auto_schema(
        operation_summary="Beneficiary list",
        tags=['assignment', 'facililator'])
    def list(self, request, pk=None):
        assignments = Assignment.objects.filter(
            project=pk).order_by('-created')
        return self.paginated_response(assignments, request)

    @swagger_auto_schema(
        operation_summary="Join to project",
        operation_description="Beneficiary sends join request to specified project",
        tags=['assignment', 'beneficiary'])
    def create(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        assignment = Assignment.objects.create(
            beneficiary=request.user,
            project=project)
        serializer = self.serializer_class(assignment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Accept or reject join request",
        request_body=AssignmentSerializer,
        tags=['assignment', 'facililator'])
    def patrial_update(self, request, pk=None):
        assignment = get_object_or_404(Assignment, pk=pk)
        serializer = self.serializer_class(assignment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

