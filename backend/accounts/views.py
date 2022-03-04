import logging
import base64
from common.views import CommonView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from transactions.models import Transaction
from django.db.models import Sum, Q
from projects.models import Project
from django.shortcuts import get_object_or_404
from decimal import *
from algorand.utils import get_transactions
from activities.models import Activity
from algosdk import util


logger = logging.getLogger(__name__)


class AccountView(CommonView):
    @swagger_auto_schema(
        operation_summary="Balance",
        tags=['accounts', 'facililator', 'beneficiary', 'investor'])
    def list(self, request):
        invest_transactions = get_transactions(
            address=request.user.account.address,
            address_role="sender",
            note_prefix="I|".encode(),
            txn_type="appl"
        )['transactions']
        print("INVEST", invest_transactions)

        app_ids = dict()
        for invest_transaction in invest_transactions:
            print("TRR", invest_transaction)
            invest_details = invest_transaction['application-transaction']
            if len(invest_details['application-args']) > 1:
                amount = base64.b64decode(
                    invest_details['application-args'][1])
                app_ids[invest_details['application-id']
                        ] = int.from_bytes(amount, "big")

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
                'balance': request.user.account.usdc_balance()
            },
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Project balance",
        tags=['accounts', 'facililator', 'investor'])
    def retrieve(self, request, pk=None):
        project = get_object_or_404(
            Project,
            pk=pk,
            investment__isnull=False)

        account = project.smartcontract.account
        balance = account.usdc_balance()
        spent = Transaction.objects.filter(
            from_account=account,
            action=Transaction.REWARD,
            status__in=[Transaction.CONFIRMED, Transaction.PENDING],
            project=project).aggregate(
                total_spent=Sum('amount')).get('total_spent', 0)
        facililator_fee = Transaction.objects.get(
            action=Transaction.FACILITATOR_FEE,
            status__in=[Transaction.CONFIRMED, Transaction.PENDING],
            project=project).amount

        return Response({
            'total': project.investment.amount,
            'balance': balance,
            'spent': spent if spent else 0,
            'facililator_fee': facililator_fee
        }, status=status.HTTP_200_OK)

    def details(self, request):
        return Response({
            "address": request.user.account.address
        }, status=status.HTTP_200_OK)
