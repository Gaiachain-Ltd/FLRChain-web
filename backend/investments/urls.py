from django.urls import path
from investments.views import *

urlpatterns = [
    path('projects/<int:pk>/investments/', InvestmentView.as_view({'post': 'create', 'get': 'retrieve'})),
    path('projects/<int:pk>/investors/',  InvestmentView.as_view({'get': 'list'}))
]