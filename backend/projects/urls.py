from django.urls import path
from projects.views import *

urlpatterns = [
    path('projects/', ProjectView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:pk>/', ProjectView.as_view({'get': 'retrieve'})),
    path('projects/<int:pk>/assignments/', AssignmentView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/assignments/<int:pk>/', AssignmentView.as_view({'put': 'patrial_update'})),
    path('projects/<int:pk>/investments/', InvestmentView.as_view({'post': 'create'})),
]