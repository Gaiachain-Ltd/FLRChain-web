from django.urls import path
from payments.views import CirclePaymentView

urlpatterns = [
    path('payment/circle/key/', CirclePaymentView.as_view({'get': 'get_key'})),
]