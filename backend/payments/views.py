import logging
from django.shortcuts import render
from common.views import CommonView
from rest_framework.permissions import IsAuthenticated
from users.permissions import isInvestor
from payments.circle import circle
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


logger = logging.getLogger(__name__)

circle_client = circle.CircleAPI(
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
            "key": circle_reply.get('data', dict()).get('publicKey', None)
        }, status=status.HTTP_200_OK)