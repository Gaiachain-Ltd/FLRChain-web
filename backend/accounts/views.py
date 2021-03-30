import logging
from common.views import CommonView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from transactions.models import Transaction
from django.db.models import Sum, Q


logger = logging.getLogger(__name__)


class AccountView(CommonView):
    @swagger_auto_schema(
        operation_summary="Balance",
        tags=['accounts', 'facililator', 'beneficiary', 'investor'])
    def list(self, request):
        account = request.user.account
        balance = account.usdc_balance()
        spent = Transaction.objects.filter(
            from_account=request.user.account,
            currency=Transaction.USDC).aggregate(
                total_spent=Sum('amount')).get('total_spent', 0)
        received = Transaction.objects.filter(
            Q(to_account=request.user.account,
              currency=Transaction.USDC) &
            ~Q(action=Transaction.FUELING)).aggregate(
                total_received=Sum('amount')).get('total_received', 0)

        return Response(
            {
                'balance': balance,
                'spent': spent - received,
                'received': received,
                'total': balance + (spent - received)
            },
            status=status.HTTP_200_OK)
