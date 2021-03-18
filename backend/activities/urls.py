from django.urls import path
from activities.views import *

urlpatterns = [
    path('projects/<int:project_pk>/tasks/<int:tasks_pk>/activities/', ActivityView.as_view({'post': 'create'})),
]