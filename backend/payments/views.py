import logging
import uuid
import hashlib
from django.shortcuts import render
from common.views import CommonView
from rest_framework.permissions import IsAuthenticated
from users.permissions import isInvestor
from payments.circle import CircleAPI
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from payments.serializers import *
from decimal import *
from payments.models import CirclePayment
from django.db import transaction
from django.shortcuts import get_object_or_404


logger = logging.getLogger(__name__)

circle_client = CircleAPI(
    settings.CIRCLE_API_KEY,
    settings.CIRCLE_API_ENVIROMENT_URL)


class CirclePaymentView(CommonView):
    permission_classes = (IsAuthenticated, isInvestor)

    @swagger_auto_schema(
        operation_summary="Get Circle public key",
        tags=['payments', 'circle', 'investor'])
    def get_key(self, request):
        circle_reply = circle_client.get_public_key()
        logger.warning("Circle reply: %s", circle_reply)
        return Response({
            **circle_reply['data']
        }, status=status.HTTP_200_OK)

    def _get_ip(request):
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
            },
            'expMonth': exp_month,
            'expYear': exp_year,
            'metadata': {
                'email': request.user.email,
                'sessionId': hashlib.sha256(request.user.id).hexdigest(),
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
                'sessionId': hashlib.sha256(request.user.id).hexdigest(),
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
