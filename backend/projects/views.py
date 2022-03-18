from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from common.views import CommonView
from projects.models import Project, Assignment
from projects.serializers import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from users.models import CustomUser
from django_filters import rest_framework as filters
from users.permissions import *
from algorand.utils import *
from algorand import smartcontract
from rest_framework import parsers
import json

class ProjectView(CommonView):
    serializer_class = ProjectSerializer
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)
    filterset_fields = ('status',)
    search_fields = ('title',)

    def get_permissions(self):
        """
        Only facililator can make and update projects.
        """
        if self.request.method in ["POST", "PUT"]:
            return [permission() for permission in [
                *self.permission_classes, isFacilitator, isOptedIn]]
        return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(
        operation_summary="Full project list",
        tags=['projects', 'facililator', 'beneficiary', 'investor'])
    def list(self, request):
        if request.user.type == CustomUser.BENEFICIARY:
            projects = Project.objects.with_beneficiary_assignment_status(
                request.user)
        elif request.user.type == CustomUser.FACILITATOR:
            projects = Project.objects.filter(
                owner=request.user).with_sum_spent_transactions()
        else:
            projects = Project.objects.for_investor(
                request.user).with_sum_spent_transactions()

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

    def image(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project.image = serializer.validated_data['image']
        project.save()

        return Response(
            ProjectSerializer(project).data, status=status.HTTP_200_OK)


class DataTypeTagView(CommonView):
    serializer_class = DataTypeTagSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, _, pk=None):
        tag = get_object_or_404(DataTypeTag, pk=pk)
        tag.delete()
        return Response(status=status.HTTP_200_OK)


class DataTagView(CommonView):
    serializer_class = DataTagSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, _, pk=None):
        tag = get_object_or_404(DataTag, pk=pk)
        tag.delete()
        return Response(status=status.HTTP_200_OK)


class AssignmentView(CommonView):
    serializer_class = AssignmentSerializer
    permission_classes = ()

    # def get_permissions(self):
    #     """
    #     Only beneficiary can make join request.
    #     Only facililator can get list of pending beneficiaries.
    #     Only facililator can accept/reject join request.
    #     """
    #     if self.request.method == "POST":
    #         return [permission() for permission in [*self.permission_classes, isBeneficiary]]
    #     elif self.request.method in ["GET", "PUT"]:
    #         return [permission() for permission in [*self.permission_classes, isFacilitator]]
    #     return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(
        operation_summary="Beneficiary list",
        tags=['assignment', 'facililator'])
    def list(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        data = smartcontract.get_beneficiaries(project.app_id)
        beneficiaries = Assignment.objects.select_related('beneficiary','beneficiary__account').filter(
            beneficiary__account__address__in=data.keys()
        ).values_list(
            "id", 
            "status",
            "sync",
            "beneficiary__id", 
            "beneficiary__first_name", 
            "beneficiary__last_name", 
            "beneficiary__account__address"
        )

        for beneficiary in beneficiaries:
            data[beneficiary[6]].update({
                "id": beneficiary[0],
                "status": beneficiary[1],
                "sync": beneficiary[2],
                "user_id": beneficiary[3],
                "name": f"{beneficiary[4]} {beneficiary[5]}",
                "address": beneficiary[6],
            })
            
        return Response(data.values(), status=status.HTTP_200_OK)

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
    def update(self, request, pk=None):
        assignment = get_object_or_404(
            Assignment, 
            pk=pk,
            status=Assignment.WAITING,
            sync=Assignment.SYNCED
        )
        serializer = self.serializer_class(assignment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sync=Assignment.TO_SYNC)
        return Response(serializer.data, status=status.HTTP_200_OK)

