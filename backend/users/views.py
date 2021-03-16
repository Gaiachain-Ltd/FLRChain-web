from rest_framework import status
from rest_framework.response import Response
from users.serializers import CustomUserSerializer
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    operation_summary="Register user",
    method='POST',
    request_body=CustomUserSerializer,
    tags=['users', 'facililator', 'beneficiary'])
@api_view(['POST'])
@permission_classes([])
def user_register(request):
    with transaction.atomic():
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    operation_summary="User info",
    method='GET',
    tags=['users', 'facililator', 'beneficiary'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)