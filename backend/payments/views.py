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
        # data = {
        #     "idempotencyKey":"45df239c-499a-42a7-9726-31fa402c6a26",
        #     "expMonth":1,
        #     "expYear":2025,
        #     "keyId":"key1",
        #     "encryptedData":"LS0tLS1CRUdJTiBQR1AgTUVTU0FHRS0tLS0tDQpWZXJzaW9uOiBPcGVuUEdQLmpzIHY0LjEwLjQNCkNvbW1lbnQ6IGh0dHBzOi8vb3BlbnBncGpzLm9yZw0KDQp3Y0JNQTBYV1NGbEZScFZoQVFmL1U3dWNBUVdVdUpkN2ZyYm9nbXBPb0s5aFhSZWd5dWZacllxOEtPRGcNCm93blJQSWJBOEhDWjgvei85VzhTNHc4eElmdHRUd05tRkNkalhjS0V5a3ZOMVdiMVFtV3ZLWWg2cmVKcA0KUTBWc2RPYzIxZ0pERUwxVUhxMTZwUGhQUktlSFQyUlFQL05IQ29DOE5qUTdPMGUzU2ZNekJ2WUtMQ2VYDQpwSEtQZFJMa3RuSHRhK05laVl5eWpkdGhBMXZtR2tOMm9yMnBnV3g4QXVvQ05VQ2RZcWxLY09YN0hqRFUNCmtZUmxOUXFLUkVIbWNuNU9qRlVhdExDMlZnc2dyMEErRzRYVDR2T0hUVFpzNHhvMkI2aVE3bUFkcTFhVA0KTzVOWnJTQ3F2TG40cThPRnJwZGRPMG40VnpxY1g3UXNNSERwQ0pMWGdVa3llK3ZMMzVPWDUxQ0Z3WXNDDQo0ZEpoQWZzUEFJQm05ZnQ0QU1DR0kraVFGcnZWeHFOanJ6U1BQREhlcEtaTEdDUVpnc2pZOEFyZWR5WDcNCndZVElsSCtsSE5MbWtBV1JNWEEvRlpZMUtEcC9hc1NzcjBWaWNsUlhNUURDWnJhUFp4UUx3azhRTlNNag0KK1JLVE5GZDNZWUcvU2c9PQ0KPXBybFgNCi0tLS0tRU5EIFBHUCBNRVNTQUdFLS0tLS0NCg==",
        #     "billingDetails":{
        #         "line1":"Test",
        #         "line2":"",
        #         "city":"Test City",
        #         "district":"MA",
        #         "postalCode":"11111",
        #         "country":"US",
        #         "name":"Customer 0001"},
        #     "metadata":{
        #         "phoneNumber":"+12025550180",
        #         "email":"customer-0001@circle.com",
        #         "sessionId":"xxx",
        #         "ipAddress":"172.33.222.1"}
        # }
        print("REQUEST SAVE CARD", data)
        circle_reply = circle_client.save_card(data)
        print("REP SAVE CARD", circle_reply)
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

        # data = {
        #     "idempotencyKey": "02ee3fff-3a78-48d5-91b1-6b9da437a6f2",
        #     "amount": {
        #         "amount": "10.00",
        #         "currency": "USD"
        #     },
        #     "verification": "cvv",
        #     "source": {
        #         "id": "24d89156-f19a-4191-944e-d4a548176375",
        #         "type": "card"
        #     },
        #     "description": "",
        #     "metadata": {
        #         "phoneNumber": "+12025550180",
        #         "email": "customer-0001@circle.com",
        #         "sessionId": "xxx",
        #         "ipAddress": "172.33.222.1"
        #     },
        #     "encryptedData": "LS0tLS1CRUdJTiBQR1AgTUVTU0FHRS0tLS0tDQpWZXJzaW9uOiBPcGVuUEdQLmpzIHY0LjEwLjQNCkNvbW1lbnQ6IGh0dHBzOi8vb3BlbnBncGpzLm9yZw0KDQp3Y0JNQTBYV1NGbEZScFZoQVFmK05yYjU3ZDR3TDNuRVQvMTVjbk5PQy9rdFVxN2Q4NDFWVjA3T25FdzgNClRmUUxmUmJtcS92SVZibTdXNUFxQ085NC92cUg2c0NDQitoUnYvdGVxcDI4TjlvaUdUc0cxdmdhR1lUTg0KNmxZbzhtTDZlcHduSldNZXB4RDRvcXhCd2VlS21YaXFMME84TEtpZUhyZE52VXhJeERHMmRYUzB0UXZtDQpPWFdlQ0x2NTdIMWNUclRmZGd2aEFpUUYwb3V3dkkrZWtHMTBVSTExTnJwZWFEMXRCalNZUzBGcllMNlANClRNcFNaMW01NEpjWHhQTUIyQVJhRHplZUVKMDZXMzAvQjBpTWRxbG1xYkJZZFFQSUdDM2VHNUtHSW1KLw0KVzlIRE0wSmpNdkd3MTJUUUt5VHkxeElqaHJ4RnNlTVZWOXhvOXEzemVoSHlMczFDZDVOeHJvWkJqYkxtDQpqdEpGQWZsRVBBVUY0b3lFZ3pVODJqNUdBd0Jtd1ppL1FWWjVwUlBabVVsa3Buck05RC9BMVMvR1JoeTYNCjRWMTkrRThSL2dtT1JzSWMrQkhkYTRiR3R6aUdFOVBnYWUyVw0KPUs5Y04NCi0tLS0tRU5EIFBHUCBNRVNTQUdFLS0tLS0NCg==",
        #     "keyId": "key1"
        # }
        print("REQUEST MAKE PAYMENT", data)
        with transaction.atomic():
            circle_reply = circle_client.create_payment(data)
            CirclePayment.objects.create(
                id=circle_reply['data']['id'],
                amount=circle_reply['data']['amount']['amount'],
                user=request.user
            )
        print("REP MAKE PAYMENT", circle_reply)
        return Response(circle_reply, status=status.HTTP_200_OK)

    def payment_info(self, request, payment_id=None):
        circle_reply = circle_client.payment_info(payment_id)
        print("REPLY PAYMENT INFO", circle_reply)
        # TODO: TESTING ONLY
        if circle_reply['data']['status'] == 'confirmed':
            amount = Decimal(circle_reply['data']['amount']['amount']).quantize(Decimal("0.01"))
            fee = Decimal(circle_reply['data']['fees']['amount']).quantize(Decimal("0.01"))
            data = {
                "idempotencyKey": str(uuid.uuid4()),
                "source": {
                    "type": "wallet",
                    "id": "1000100943",
                },
                "destination": {
                    "type": "blockchain",
                    "address": request.user.account.address,
                    "chain": "ALGO"
                },
                "amount": {
                    "amount": str(Decimal(amount - fee).quantize(Decimal("0.01"))),
                    "currency": "USD"
                }
            }
            print("REQUEST USDC TRANSFER", data)
            circle_reply2 = circle_client.transfer_usdc(data)
            print("REPLY USDC TRANSFER", circle_reply2)
        return Response(circle_reply, status=status.HTTP_200_OK)