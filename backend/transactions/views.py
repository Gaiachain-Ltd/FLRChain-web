import logging
import datetime
from decimal import *
from common.views import CommonView
from transactions.models import Transaction
from django.db.models import Q
from transactions.serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from algorand.utils import get_transactions


logger = logging.getLogger(__name__)


class TransactionView(CommonView):
    serializer_class = TransactionSerializer

    @swagger_auto_schema(
        operation_summary="Full transaction list",
        tags=['transactions', 'facililator', 'beneficiary', 'investor'])
    def list(self, request):
        # Fetch transactions from indexer:
        algo_txns = get_transactions(
            request.user.account.address,
            limit=None # TODO: Add pagination
        )

        # Parse each transaction:
        txids = list()
        transactions = dict()
        for algo_txn in algo_txns['transactions']:
            txid = algo_txn['id']
            received = algo_txn['asset-transfer-transaction']['receiver'] == request.user.account.address

            transactions[txid] = {
                "id": txid,
                "txid": txid,
                "action": 8 if received else 9,
                "created": datetime.datetime.fromtimestamp(algo_txn['round-time']),
                "amount": Decimal(algo_txn['asset-transfer-transaction']['amount']) / Decimal(1000000),
                "project_name": "",
                "status": Transaction.CONFIRMED
            }
            txids.append(txid)

        # Obtain details from database:
        flr_transactions = Transaction.objects.filter(
            Q(from_account=request.user.account) | Q(
                to_account=request.user.account),
            ~Q(action__in=[Transaction.OPT_IN]),
            currency=Transaction.USDC, txid__in=txids).order_by('-created')

        # Update parsed transactions with project details:
        for flr_transaction in flr_transactions:
            algo_txn = transactions.get(flr_transaction.txid, None)
            if algo_txn is None:
                continue

            if flr_transaction.project:
                algo_txn["project_name"] = flr_transaction.project.title

            algo_txn["action"] = flr_transaction.action
            algo_txn["status"] = flr_transaction.status

            transactions[flr_transaction.txid] = algo_txn

        return self.paginated_response(list(transactions.values()), request)
