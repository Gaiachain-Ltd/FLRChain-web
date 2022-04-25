import logging
import base64
import datetime
from common.views import CommonView, NoGetQueryParametersSchema
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Sum
from projects.models import Project
from decimal import *
from algorand.utils import get_transactions, application_address, INDEXER
from activities.models import Activity
from algosdk import util
from rest_framework import status
from django.http import HttpResponse
from accounts.serializers import *
from django.conf import settings
from collections import defaultdict


logger = logging.getLogger(__name__)


class AccountView(CommonView):
    @swagger_auto_schema(
        auto_schema=NoGetQueryParametersSchema,
        operation_summary="User balance",
        operation_description=("User's account balance in USDC"),
        tags=['accounts', 'facililator', 'beneficiary', 'investor'],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'balance': openapi.Schema(
                        type=openapi.TYPE_INTEGER
                    ),
                    'address': openapi.Schema(
                        type=openapi.TYPE_STRING
                    )
                }
            ),
        }
    )
    def balance(self, request):
        return Response(
            {
                'balance': request.user.account.usdc_balance(),
                'address': request.user.account.address
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        auto_schema=NoGetQueryParametersSchema,
        operation_summary="Investor balance",
        operation_description=(""),
        tags=['accounts', 'investor'],
    )
    def details(self, request):
        invest_transactions = get_transactions(
            address=request.user.account.address,
            address_role="sender",
            note_prefix="I|".encode(),
            txn_type="appl"
        )['transactions']

        app_ids = defaultdict(lambda: 0)
        for invest_transaction in invest_transactions:
            invest_details = invest_transaction['application-transaction']
            if len(invest_details['application-args']) > 1:
                amount = base64.b64decode(
                    invest_details['application-args'][1])
                app_ids[invest_details['application-id']
                        ] += int.from_bytes(amount, "big")

        projects = Project.objects.filter(
            app_id__in=app_ids.keys()
        )

        distributed = Activity.objects.filter(
            project__in=projects
        ).aggregate(distributed=Sum('reward'))['distributed']

        allocated = 0
        for project in projects:
            amount = app_ids.get(project.app_id, None)
            if amount:
                allocated += amount

        return Response(
            {
                'allocated': util.microalgos_to_algos(allocated),
                'distributed': distributed,
                'balance': request.user.account.usdc_balance(),
                "address": request.user.account.address
            },
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        auto_schema=NoGetQueryParametersSchema,
        operation_summary="User's wallet QR code",
        tags=['accounts', 'beneficiary'],
    )
    def qr_code(self, request):
        response = HttpResponse(
            request.user.account.qr_code, content_type='image/svg+xml')
        response['Content-Disposition'] = 'attachment; filename="code.svg"'
        return response


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
                "project_name": project[1]
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
                    note = transaction.get('note', "")
                    transaction = inner_transactions[0]
                    transaction['id'] = txid
                    transaction['note'] = note

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
                "note": base64.b64decode(transaction.get("note", "")).decode(),
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
