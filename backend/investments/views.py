from django.shortcuts import get_object_or_404
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from investments.serializers import InvestmentSerializer
from common.views import CommonView
from projects.models import Project
from investments.models import Investment
from rest_framework.response import Response
from django.db import transaction
from smart_contracts.models import SmartContract
from users.permissions import isInvestor, isOptedIn
from rest_framework.permissions import IsAuthenticated
from algorand.smartcontract import invest, opted_in_addresses
from django.db.models import Q
from users.models import CustomUser
from algorand.utils import get_transactions_info, get_transactions, application_address
import datetime
from django.conf import settings


class InvestmentView(CommonView):
    serializer_class = InvestmentSerializer
    # permission_classes = [IsAuthenticated, isInvestor, isOptedIn]

    def list(self, _, pk=None):
        project = get_object_or_404(
            Project,
            pk=pk
        )
        if project.state == Project.INITIAL:
            return Response([], status=status.HTTP_200_OK)

        data = get_transactions_info(
            request_fields={
                "address": application_address(project.app_id),
                "address_role": "receiver",
                "asset_id": settings.ALGO_ASSET,
                "min_amount": 1
            },
            reply_fields=[
                "sender",
                "asset-transfer-transaction__amount",
                "round-time",
                "id"
            ]
        )

        investors = CustomUser.objects.select_related('account').filter(
            account__address__in=data.keys()
        ).values_list('first_name', 'last_name', 'account__address')

        for investor in investors:
            data[investor[2]]['name'] = f"{investor[0]} {investor[1]}"

        return Response(data.values(), status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Invest in project",
        request_body=InvestmentSerializer,
        tags=['investor'])
    def create(self, request, pk=None):
        project = get_object_or_404(
            Project,
            pk=pk,
            status=Project.FUNDRAISING,
            state__in=(Project.INITIALIZED, Project.POSTPONED)
        )
        account = request.user.account
        invest(
            account.address,
            account.private_key,
            project.app_id,
            int(request.data.get('amount'))
        )

        # with transaction.atomic():
        #     serializer = self.serializer_class(data=request.data)
        #     serializer.is_valid(raise_exception=True)

        #     start = serializer.validated_data['start']
        #     end = serializer.validated_data['end']

        #     project = get_object_or_404(
        #         Project,
        #         pk=pk,
        #         investment=None,
        #         start__lte=start,
        #         end__gte=end)

        #     investment = Investment.objects.create(
        #         project=project,
        #         investor=request.user,
        #         amount=serializer.validated_data['amount'],
        #         start=start,
        #         end=end)

        #     SmartContract.generate(investment)

        #     serializer = self.serializer_class(investment)
        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Investment details",
        tags=['investor'])
    def retrieve(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)

        investors = opted_in_addresses(
            project.app_id).get(CustomUser.INVESTOR, [])
        return Response(
            {
                "invested": request.user.account.address in investors
            },
            status=status.HTTP_200_OK
        )
