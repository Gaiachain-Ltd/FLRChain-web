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
from algorand.utils import get_transactions, application_address
from django.conf import settings
from projects.models import Project


logger = logging.getLogger(__name__)


class TransactionView(CommonView):
    serializer_class = TransactionSerializer

    @swagger_auto_schema(
        operation_summary="Full transaction list",
        tags=['transactions', 'facililator', 'beneficiary', 'investor'])
    def list(self, request):
        requestor_address = request.user.account.address

        participations = get_transactions(
            address=request.user.account.address,
            address_role="sender",
            txn_type="appl"
        )['transactions']
        app_ids = list()
        for participation in participations:
            app_transaction_details = participation['application-transaction']
            app_ids.append(app_transaction_details['application-id'])

        projects = Project.objects.filter(app_id__in=app_ids).values_list(
            'id',
            'title',
            'app_id'
        )
        project_dict = dict()
        for project in projects:
            project_dict[application_address(project[2])] = {
                "project_id": project[0],
                "project_title": project[1]
            }

        transactions = get_transactions(
            address=request.user.account.address,
            asset_id=settings.ALGO_ASSET,
            min_amount=1,
            txn_type="axfer"
        )['transactions']
        data = list()
        for transaction in transactions:
            # TODO: Handle inner transactions:
            if transaction.get('asset-transfer-transaction', None) is None:
                continue
            asset_transaction_details = transaction['asset-transfer-transaction']
            received = requestor_address == asset_transaction_details['receiver']
            data.append({
                "id": transaction['id'],
                "action": 1 if received else 2,
                "round-time": transaction['round-time'],
                "amount": asset_transaction_details['amount'],
                **project_dict.get(
                    transaction['sender'] if received else asset_transaction_details['receiver'],
                    {}
                )
            })
        return Response(data, status=status.HTTP_200_OK)
        # Fetch transactions from indexer:
        # algo_txns = get_transactions(
        #     request.user.account.address,
        #     limit=None # TODO: Add pagination
        # )

        # # Parse each transaction:
        # txids = list()
        # transactions = dict()
        # for algo_txn in algo_txns['transactions']:
        #     txid = algo_txn['id']
        #     received = algo_txn['asset-transfer-transaction']['receiver'] == request.user.account.address

        #     transactions[txid] = {
        #         "id": txid,
        #         "txid": txid,
        #         "action": 8 if received else 9,
        #         "created": datetime.datetime.fromtimestamp(algo_txn['round-time']),
        #         "amount": Decimal(algo_txn['asset-transfer-transaction']['amount']) / Decimal(1000000),
        #         "project_name": "",
        #         "status": Transaction.CONFIRMED
        #     }
        #     txids.append(txid)

        # # Obtain details from database:
        # flr_transactions = Transaction.objects.filter(
        #     Q(from_account=request.user.account) | Q(
        #         to_account=request.user.account),
        #     ~Q(action__in=[Transaction.OPT_IN]),
        #     currency=Transaction.USDC, txid__in=txids).order_by('-created')

        # # Update parsed transactions with project details:
        # for flr_transaction in flr_transactions:
        #     algo_txn = transactions.get(flr_transaction.txid, None)
        #     if algo_txn is None:
        #         continue

        #     if flr_transaction.project:
        #         algo_txn["project_name"] = flr_transaction.project.title

        #     algo_txn["action"] = flr_transaction.action
        #     algo_txn["status"] = flr_transaction.status

        #     transactions[flr_transaction.txid] = algo_txn

        # return self.paginated_response(list(transactions.values()), request)
