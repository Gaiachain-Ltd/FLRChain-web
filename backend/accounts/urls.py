from django.urls import path
from accounts.views import AccountView

urlpatterns = [
    path('accounts/qrcode/', AccountView.as_view({'get': 'qr_code'})),
    path('accounts/details/', AccountView.as_view({'get': 'details'})),
    path('accounts/balance/', AccountView.as_view({'get': 'balance'})),
]