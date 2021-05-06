import logging
from common.views import CommonView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from transactions.models import Transaction
from django.db.models import Sum, Q
from projects.models import Project
from django.shortcuts import  get_object_or_404


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
            currency=Transaction.USDC,
            status__in=[Transaction.CONFIRMED, Transaction.PENDING]).aggregate(
                total_spent=Sum('amount')).get('total_spent', 0)
        received = Transaction.objects.filter(
            Q(to_account=request.user.account,
              currency=Transaction.USDC,
              status__in=[Transaction.CONFIRMED, Transaction.PENDING]) &
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