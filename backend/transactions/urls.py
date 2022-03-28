from django.urls import path
from transactions.views import *

urlpatterns = [
    path('transactions/', TransactionView.as_view({'get': 'list'})),
    path('transactions/<str:id>/', TransactionView.as_view({'get': 'retrieve'})),
]