import logging
import uuid
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
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Get Circle public key",
        tags=['payments', 'circle', 'investor'])
    def get_key(self, request):
        circle_reply = circle_client.get_public_key()
        logger.warning("Circle reply: %s", circle_reply)
        return Response({
            **circle_reply['data']
        }, status=status.HTTP_200_OK)

    def save_card(self, request):
        serializer = SaveCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data =  {
            'idempotencyKey': serializer.validated_data['idempotencyKey'],
            'keyId': serializer.validated_data['keyId'],
            'encryptedData': serializer.validated_data['encryptedData'],
            'billingDetails': {
                'name': serializer.validated_data['billingDetails']['name'],
                'city': serializer.validated_data['billingDetails']['city'],
                'country': serializer.validated_data['billingDetails']['country'],
                'line1': serializer.validated_data['billingDetails']['line1'],
                'line2': serializer.validated_data['billingDetails'].get('line2', ''),
                'district': serializer.validated_data['billingDetails'].get('district', ''),
                'postalCode': serializer.validated_data['billingDetails']['postalCode'],
            },
            'expMonth': 10,
            'expYear': 2022,
            'metadata': {
                'email': request.user.email,
                'phoneNumber': '+48663317345',
                'sessionId': 'DE6FA86F60BB47B379307F851E238617',
                'ipAddress': '127.0.0.1'
            }
        }

        circle_reply = circle_client.save_card(data)
        return Response(circle_reply, status=status.HTTP_200_OK)

    def make_payment(self, request):
        serializer = MakePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'idempotencyKey': serializer.validated_data['idempotencyKey'],
            'amount': {
                'amount': str(serializer.validated_data['amount']),
                'currency': 'USD'
            },
            'verification': 'none',
            'source': {
                'id': serializer.validated_data['cardId'],
                'type': 'card'
            },
            'description': 'FLRChain test payment.',
            'metadata': {
                'email': request.user.email,
                'phoneNumber': '+48663317345',
                'sessionId': 'DE6FA86F60BB47B379307F851E238617',
                'ipAddress': '127.0.0.1'
            },
            'encryptedData': serializer.validated_data['encryptedData'],
            'keyId': serializer.validated_data['keyId'],
        }

        with transaction.atomic():
            circle_reply = circle_client.create_payment(data)
            CirclePayment.objects.create(
                id=circle_reply['data']['id'],
                amount=circle_reply['data']['amount']['amount'],
                user=request.user
            )

        return Response(circle_reply, status=status.HTTP_200_OK)