from django.urls import path
from payments.views import CirclePaymentView

urlpatterns = [
    path('payments/circle/key/', CirclePaymentView.as_view({'get': 'get_key'})),
]