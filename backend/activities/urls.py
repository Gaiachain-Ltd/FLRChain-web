from django.urls import path
from activities.views import *

urlpatterns = [
    path('projects/<int:project_pk>/activities/<str:activity_pk>/',
         ActivityView.as_view({'put': 'update'})),
    path('projects/<int:project_pk>/distributed/',
         ActivityView.as_view({'get': 'distributed'})),
    path('projects/<int:pk>/activities/',
         ActivityView.as_view({'get': 'list'})),
    path('projects/<int:project_pk>/tasks/<int:task_pk>/activities/',
         ActivityView.as_view({'get': 'task_activities', 'post': 'create'})),
    path('projects/activity/<uuid:activity_pk>/photo/',
         PhotoView.as_view({'get': 'list', 'post': 'create'}))
]
