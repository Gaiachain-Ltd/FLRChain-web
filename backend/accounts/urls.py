from django.urls import path
from accounts.views import AccountView

urlpatterns = [
    path('accounts/details/', AccountView.as_view({'get': 'details'})),
    path('accounts/', AccountView.as_view({'get': 'list'})),
    path('projects/<int:pk>/accounts/', AccountView.as_view({'get': 'retrieve'}))
]