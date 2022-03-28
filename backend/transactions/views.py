import logging
import datetime
from decimal import *
from common.views import CommonView, NoGetQueryParametersSchema
from transactions.models import Transaction
from django.db.models import Q
from transactions.serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from algorand.utils import get_transactions, application_address, INDEXER
from django.conf import settings
from projects.models import Project
from algosdk import util

logger = logging.getLogger(__name__)


class TransactionView(CommonView):
    serializer_class = TransactionSerializer

    @swagger_auto_schema(
        auto_schema=NoGetQueryParametersSchema,
        operation_summary="Transaction list",
        responses={
            status.HTTP_200_OK: TransactionSerializer
        },
        tags=['transactions', 'beneficiary', 'facililator', 'investor'])
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
            if transaction.get('inner-txns', None):
                inner_transactions = transaction['inner-txns']
                if len(inner_transactions) > 0:
                    txid = transaction['id']
                    transaction = inner_transactions[0]
                    transaction['id'] = txid

            if transaction.get('asset-transfer-transaction', None) is None:
                continue
                    
            asset_transaction_details = transaction['asset-transfer-transaction']
            received = requestor_address == asset_transaction_details['receiver']
            data.append({
                "id": transaction['id'],
                "action": 1 if received else 2,
                "created": datetime.datetime.utcfromtimestamp(
                    transaction['round-time']
                ).strftime('%Y-%m-%d %H:%M:%S'),
                "amount": util.microalgos_to_algos(
                    asset_transaction_details['amount']
                ),
                **project_dict.get(
                    transaction['sender'] if received else asset_transaction_details['receiver'],
                    {}
                )
            })
        return Response(
            TransactionSerializer(data, many=True).data, 
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        auto_schema=NoGetQueryParametersSchema,
        operation_summary="Transaction info",
        operation_description=("Returns null if transaction is not confirmed yet."
         " Otherwise, returns a transaction details."
        ),
        tags=['transactions', 'beneficiary', 'facililator', 'investor']
    )
    def retrieve(self, _, id=None):
        try:
            reply = INDEXER.transaction(id)
        except:
            reply = None

        return Response(
            {'details': reply},
            status=status.HTTP_200_OK
        )
