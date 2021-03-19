from django.urls import path
from activities.views import *

urlpatterns = [
    path('projects/<int:pk>/activities/', ActivityView.as_view({'get': 'list'})),
    path('projects/<int:project_pk>/tasks/<int:task_pk>/activities/', ActivityView.as_view({'post': 'create'})),
]