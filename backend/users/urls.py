from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users.views import CustomUserView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', CustomUserView.as_view(), name='register')
]
