from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users.views import *
from drf_yasg.utils import swagger_auto_schema

decorated_token_view = swagger_auto_schema(
      operation_summary="Login user",
      method='POST',
      tags=['users', 'facililator', 'beneficiary', 'investor'])(obtain_auth_token)

urlpatterns = [
    path('login/', decorated_token_view, name='login'),
    path('register/', user_register, name='register'),
    path('info/', user_info, name='info')
]
