from django.shortcuts import get_object_or_404
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from investments.serializers import InvestmentSerializer
from common.views import CommonView
from projects.models import Project
from investments.models import Investment
from rest_framework.response import Response
from users.permissions import isInvestor, isOptedIn
from django.db.models import Sum
from users.models import CustomUser
from algorand.utils import get_transactions
import base64
from algosdk import util
from collections import defaultdict


class InvestmentView(CommonView):
    serializer_class = InvestmentSerializer

    def get_permissions(self):
        """
        Only facililator can update activities but only beneficiary can create them.
        """
        if self.request.method == "POST":
            return [permission() for permission in [
                *self.permission_classes, isInvestor, isOptedIn]]
        return [permission() for permission in self.permission_classes]

    def list(self, _, pk=None):
        project = get_object_or_404(
            Project,
            pk=pk
        )
        if project.state == Project.INITIAL:
            return Response([], status=status.HTTP_200_OK)

        transactions = get_transactions(
            application_id=project.app_id,
            note_prefix="I|".encode()
        )['transactions']

        data = defaultdict(list)
        for transaction in transactions:
            transaction_details = transaction['application-transaction']
            if len(transaction_details['application-args']) > 1:
                data[transaction['sender']].append({
                    'sender': transaction['sender'],
                    'name': transaction['sender'],
                    'round-time': transaction['round-time'],
                    'amount': int.from_bytes(
                        base64.b64decode(transaction_details['application-args'][1]
                                         ), "big"
                    ),
                    'id': transaction['id']
                })

        investors = CustomUser.objects.select_related('account').filter(
            account__address__in=data.keys()
        ).values_list('first_name', 'last_name', 'account__address')

        for investor in investors:
            transactions = data.get(investor[2], [])
            for transaction in transactions:
                transaction['name'] = f"{investor[0]} {investor[1]}"

        investments = list()
        for transactions in data.values():
            investments.extend(transactions)

        return Response(investments, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Invest in project",
        request_body=InvestmentSerializer,
        tags=['investor'])
    def create(self, request, pk=None):
        project = get_object_or_404(
            Project,
            pk=pk,
            status__in=(Project.FUNDRAISING, Project.ACTIVE),
            state__in=(Project.INITIALIZED, Project.POSTPONED, Project.STARTED)
        )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        Investment.objects.create(
            project=project,
            investor=request.user,
            amount=serializer.validated_data['amount']
        )

        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Investment details",
        tags=['investor'])
    def retrieve(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)

        transactions = get_transactions(
            application_id=project.app_id,
            address=request.user.account.address,
            address_role="sender",
            note_prefix="I|".encode(),
        )['transactions']

        sum = 0
        for transaction in transactions:
            transaction_details = transaction['application-transaction']
            if len(transaction_details['application-args']) > 1:
                amount = int.from_bytes(
                    base64.b64decode(transaction_details['application-args'][1]
                                     ), "big"
                )
                sum += util.microalgos_to_algos(amount)

        investments = Investment.objects.filter(
            project=project,
            investor=request.user).exclude(
                sync__in=(Investment.SYNCED, Investment.FAILED)
        )

        sync = Investment.SYNCED
        if investments.exists():
            sync = investments.first().sync

        return Response(
            {
                "sync": sync,
                "amount": sum,
            },
            status=status.HTTP_200_OK
        )
