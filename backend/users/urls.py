from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users.views import *

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', user_register, name='register'),
    path('info/', user_info, name='info')
]
