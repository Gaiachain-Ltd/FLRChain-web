import logging
from common.views import CommonView
from transactions.models import Transaction
from django.db.models import Q
from transactions.serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


logger = logging.getLogger(__name__)


class TransactionView(CommonView):
    serializer_class = TransactionSerializer
    @swagger_auto_schema(
        operation_summary="Full transaction list",
        tags=['transactions', 'facililator', 'beneficiary', 'investor'])
    def list(self, request):
        transactions = Transaction.objects.filter(
            Q(from_account=request.user.account) | Q(to_account=request.user.account),
            currency=Transaction.USDC)
        return self.paginated_response(transactions, request)