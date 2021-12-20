import logging
import hashlib
from common.views import CommonView
from rest_framework.permissions import IsAuthenticated
from users.permissions import isInvestor, isBeneficiary
from payments.circle import CircleAPI
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from payments.serializers import *
from decimal import *
from payments.models import CirclePayment, MTNPayout
from django.db import transaction
from payments.mtn import MTNAPI


logger = logging.getLogger(__name__)


circle_client = CircleAPI(
    settings.CIRCLE_API_KEY,
    settings.CIRCLE_API_ENVIROMENT_URL
)


mtn_client = MTNAPI(
    settings.MTN_SUBSCRIPTION_KEY,
    settings.MTN_API_KEY,
    settings.MTN_USER_ID,
    settings.MTN_URL,
    settings.MTN_CALLBACK_HOST
)


class CirclePaymentView(CommonView):
    permission_classes = (IsAuthenticated, isInvestor)

    @swagger_auto_schema(
        operation_summary="Get Circle public key",
        tags=['payments', 'circle', 'investor'])
    def get_key(self, request):
        circle_reply = circle_client.get_public_key()
        logger.debug("Get key reply: %s", circle_reply)
        return Response({
            **circle_reply['data']
        }, status=status.HTTP_200_OK)

    def _get_ip(self, request):
        ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip

    @swagger_auto_schema(
        operation_summary="Save credit card in Circle system",
        request_body=SaveCardSerializer,
        tags=['payments', 'circle', 'investor'])
    def save_card(self, request):
        serializer = SaveCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        expiration = serializer.validated_data['expiry']
        exp_parts = expiration.split('/')
        exp_month = int(exp_parts[0])
        exp_year = int(exp_parts[1])

        data = {
            'idempotencyKey': serializer.validated_data['idempotencyKey'],
            'keyId': serializer.validated_data['keyId'],
            'encryptedData': serializer.validated_data['encryptedData'],
            'billingDetails': {
                'name': serializer.validated_data['billingDetails']['name'],
                'city': serializer.validated_data['billingDetails']['city'],
                'country': serializer.validated_data['billingDetails']['country'],
                'line1': serializer.validated_data['billingDetails']['address'],
                'postalCode': serializer.validated_data['billingDetails']['postalCode'],
                'district': serializer.validated_data['billingDetails'].get('district', ""),
            },
            'expMonth': exp_month,
            'expYear': exp_year,
            'metadata': {
                'email': request.user.email,
                'sessionId': hashlib.md5(
                    str(request.user.id).encode('utf-8')).hexdigest(),
                'ipAddress': self._get_ip(request)
            }
        }
        logger.debug("Save card request: %s", data)

        circle_reply = circle_client.save_card(data)
        logger.debug("Save card reply: %s", circle_reply)
        return Response(circle_reply, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Make payment",
        request_body=MakePaymentSerializer,
        tags=['payments', 'circle', 'investor'])
    def make_payment(self, request):
        serializer = MakePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'idempotencyKey': serializer.validated_data['idempotencyKey'],
            'amount': {
                'amount': str(serializer.validated_data['amount']),
                'currency': 'USD'
            },
            'verification': 'cvv',
            'source': {
                'id': serializer.validated_data['cardId'],
                'type': 'card'
            },
            'description': 'FLRChain top up.',
            'metadata': {
                'email': request.user.email,
                'sessionId': hashlib.md5(
                    str(request.user.id).encode('utf-8')).hexdigest(),
                'ipAddress': self._get_ip(request)
            },
            'encryptedData': serializer.validated_data['encryptedData'],
            'keyId': serializer.validated_data['keyId'],
        }
        logger.debug("Make payment request: %s", data)

        with transaction.atomic():
            circle_reply = circle_client.create_payment(data)
            logger.debug("Make payment reply: %s", circle_reply)
            CirclePayment.objects.create(
                id=circle_reply['data']['id'],
                amount=circle_reply['data']['amount']['amount'],
                user=request.user
            )

        return Response(circle_reply, status=status.HTTP_200_OK)


class MTNPayoutView(CommonView):
    permission_classes = (IsAuthenticated, isBeneficiary)
    serializer_class = MakePayoutSerializer

    def payout(self, request):
        serializer = MakePayoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        if request.user.account.usdc_balance() < Decimal(amount):
            success = False
        else:
            MTNPayout.payout(
                request.user,
                amount,
                serializer.validated_data['phone']
            )
            success = True

        return Response({"success": success}, status=status.HTTP_200_OK)
