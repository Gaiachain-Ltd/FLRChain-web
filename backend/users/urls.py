from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import status
from users.views import *
from drf_yasg.utils import swagger_auto_schema
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from users.serializers import PasswordReplySerializer

decorated_token_view = swagger_auto_schema(
    operation_summary="Login user",
    method='POST',
    tags=['users', 'facililator', 'beneficiary', 'investor'])(obtain_auth_token)


decorated_password_reset_view = swagger_auto_schema(
    operation_summary="Request reset password link",
    operation_description="Returns 'OK' string on success",
    responses={
        status.HTTP_200_OK: PasswordReplySerializer
    },
    method='POST',
    tags=['users', 'facililator', 'beneficiary', 'investor'])(reset_password_request_token)


decorated_change_password_view = swagger_auto_schema(
    operation_summary="Change password",
    operation_description="Returns 'OK' string on success",
    responses={
        status.HTTP_200_OK: PasswordReplySerializer
    },
    method='POST',
    tags=['users', 'facililator', 'beneficiary', 'investor'])(reset_password_confirm)


urlpatterns = [
    path('login/', decorated_token_view, name='login'),
    path('register/', user_register, name='register'),
    path(
        'info/', UserInfoView.as_view({'get': 'list', 'post': 'update'}), name='info'),
    path('organization/',
         OrganizationView.as_view({'get': 'list', 'patch': 'patrial_update'})),
    path('password_reset/', decorated_password_reset_view, name="reset_password"),
    path('password_reset/confirm/',
         decorated_change_password_view, name="reset_change_password"),
    path('change_password/', change_password, name='change_password')
]
