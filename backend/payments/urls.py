from django.urls import path
from payments.views import CirclePaymentView

urlpatterns = [
    path('payments/circle/key/', CirclePaymentView.as_view({'get': 'get_key'})),
    path('payments/circle/card/payment/', CirclePaymentView.as_view({'post': 'make_payment'})),
    path('payments/circle/card/', CirclePaymentView.as_view({'post': 'save_card'})),
]