from django.urls import path
from projects.views import *

urlpatterns = [
    path('projects/', ProjectView.as_view()),
]