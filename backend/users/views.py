from rest_framework import status
from rest_framework.response import Response
from users.models import Organization
from users.serializers import *
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from accounts.models import Account
from common.views import CommonView, NoGetQueryParametersSchema


@swagger_auto_schema(
    operation_summary="Register user",
    method='POST',
    request_body=UserSerializer,
    tags=['users', 'facililator', 'beneficiary', 'investor']
)
@api_view(['POST'])
@permission_classes([])
def user_register(request):
    with transaction.atomic():
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        Account.generate(user)

        return Response(status=status.HTTP_201_CREATED)


class UserInfoView(CommonView):
    serializer_class= UserInfoSerializer

    @swagger_auto_schema(
        auto_schema=NoGetQueryParametersSchema,
        operation_summary="Get user profile",
        responses={
            status.HTTP_200_OK: UserInfoSerializer
        },
        tags=['users', 'facililator', 'beneficiary', 'investor']
    )
    def list(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update user profile",
        request_body=UserInfoSerializer,
        responses={
            status.HTTP_200_OK: UserInfoSerializer
        },
        tags=['users', 'facililator', 'beneficiary', 'investor']
    )
    def update(self, request):
        serializer = UserInfoSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganizationView(CommonView):
    serializer_class = OrganizationSerializer

    def list(self, request):
        organization, _ = Organization.objects.get_or_create(
            user=request.user
        )

        return Response(
            OrganizationSerializer(organization).data,
            status=status.HTTP_200_OK
        )

    def patrial_update(self, request, pk=None):
        organization, _ = Organization.objects.get_or_create(
            user=request.user
        )

        serializer = OrganizationSerializer(organization, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
