from django.urls import path
from payments.views import CirclePaymentView, MTNPayoutView, FacilitatorPayoutView, WalletPayoutView

urlpatterns = [
    path('payments/circle/key/', CirclePaymentView.as_view({'get': 'get_key'})),
    path('payments/circle/card/payment/', CirclePaymentView.as_view({'post': 'make_payment'})),
    path('payments/circle/card/', CirclePaymentView.as_view({'post': 'save_card'})),
    path('payments/mtn/payout/', MTNPayoutView.as_view({'post': 'payout'})),
    path('payments/facililator/', FacilitatorPayoutView.as_view({'get': 'list', 'post': 'payout'})),
    path('payments/wallet/payout/', WalletPayoutView.as_view({'post': 'payout'}))
]