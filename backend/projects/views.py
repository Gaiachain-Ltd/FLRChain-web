from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from common.views import CommonView, NoGetQueryParametersSchema
from projects.models import Project, Assignment
from projects.serializers import *
from drf_yasg.utils import swagger_auto_schema
from users.models import CustomUser
from users.permissions import *
from algorand.utils import *
from algorand import smartcontract
from rest_framework import parsers
from PIL import Image, ImageOps
from django.core.files import File
from io import BytesIO


class ProjectView(CommonView):
    serializer_class = ProjectSerializer
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)
    search_fields = ('title',)

    # def get_permissions(self):
    #     """
    #     Only facililator can make and update projects.
    #     """
    #     if self.request.method in ["POST", "PUT"]:
    #         return [permission() for permission in [
    #             *self.permission_classes, isFacilitator, isOptedIn]]
    #     return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(
        auto_schema=NoGetQueryParametersSchema,
        operation_summary="Project list",
        responses={
            status.HTTP_200_OK: ProjectSerializer(many=True)
        },
        tags=['projects', 'facililator', 'beneficiary', 'investor'],
    )
    def list(self, request):
        if request.user.type == CustomUser.BENEFICIARY:
            projects = Project.objects.with_beneficiary_assignment_status(
                request.user)
        elif request.user.type == CustomUser.FACILITATOR:
            projects = Project.objects.filter(owner=request.user)
        else:
            projects = Project.objects.for_investor(request.user)

        status_filter = request.GET.get('status', None)
        if status_filter:
            status_filter = int(status_filter)
            if request.user.type == CustomUser.INVESTOR:
                if status_filter == Project.FUNDRAISING:
                    projects = projects.filter(
                        invested=False, status=status_filter
                    )
                elif status_filter == Project.ACTIVE:
                    projects = projects.filter(
                        invested=True, 
                        status__in=[Project.FUNDRAISING, Project.ACTIVE]
                    )
                else:
                    projects = projects.filter(
                        invested=True, status=status_filter
                    )
            else:
                projects = projects.filter(status=status_filter)

        if request.GET.get('nodetails', None):
            self.serializer_class = ProjectNoDetailsSerializer

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
        responses={
            status.HTTP_200_OK: ProjectSerializer()
        },
        tags=['projects', 'facililator', 'beneficiary', 'investor'])
    def retrieve(self, request, pk=None):
        if request.user.type == CustomUser.BENEFICIARY:
            project = Project.objects.with_beneficiary_assignment_status(
                request.user).filter(pk=pk).first()
        elif request.user.type == CustomUser.FACILITATOR:
            project = Project.objects.filter(
                pk=pk, 
                owner=request.user
            ).first()
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
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        serializer = self.serializer_class(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def image(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        serializer = ProjectImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Compress image:
        im = Image.open(serializer.validated_data['image'])
        im = im.convert('RGB')
        im = ImageOps.exif_transpose(im)
        im_io = BytesIO()
        im.save(im_io, 'JPEG', quality=65)
        new_image = File(im_io, name=project.image.name)
        project.image = new_image
        project.save()

        return Response(
            ProjectSerializer(project).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="My tasks",
        operation_description="Returns list of active projects tasks from given ids in request",
        request_body=MyTasksRequestSerializer,
        responses={
            status.HTTP_200_OK: TaskSerializer
        },
        tags=['projects', 'beneficiary']
    )
    def my_tasks(self, request):
        serializer = MyTasksRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        projects = Project.objects.with_beneficiary_assignment_status(
            request.user
        ).filter(
            status=Project.ACTIVE,
            assignment_status=Assignment.ACCEPTED
        ).values_list('id', flat=True)

        tasks = Task.objects.filter(
            id__in=serializer.validated_data['ids'],
            project__id__in=projects,
            deleted=False
        )

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def close_project(self, request, pk=None):
        project = get_object_or_404(
            Project, 
            state=Project.POSTPONED,
            status=Project.FUNDRAISING,
            owner=request.user,
            pk=pk
        )

        project.status = Project.CLOSED
        project.state = Project.FINISHED
        project.sync = Project.TO_SYNC
        project.save()

        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_200_OK
        )


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
            beneficiary__account__address__in=data.keys(),
            project=project
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
        operation_description="Beneficiary sends EMPTY POST request to join to specified project",
        responses={
            status.HTTP_201_CREATED: AssignmentSerializer
        },
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

