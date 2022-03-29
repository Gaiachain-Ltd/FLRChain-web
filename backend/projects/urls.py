from django.urls import path
from projects.views import *

urlpatterns = [
    path('projects/', ProjectView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:pk>/', ProjectView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('projects/<int:pk>/assignments/', AssignmentView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/assignments/<int:pk>/', AssignmentView.as_view({'put': 'update'})),
    path('projects/datatypetag/', DataTypeTagView.as_view({'post': 'create', 'delete': 'destroy'})),
    path('projects/datatag/', DataTagView.as_view({'post': 'create', 'delete': 'destroy'})),
    path('projects/<int:pk>/image/', ProjectView.as_view({'put': 'image'})),
    path('projects/tasks/', ProjectView.as_view({'post': 'my_tasks'})),
]