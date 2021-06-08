import logging
import uuid
from celery import shared_task
from payments.circle import CircleAPI
from payments.models import CirclePayment, CircleTransfer
from django.db import models, transaction
from django.conf import settings
from decimal import *
from transactions.models import Transaction


logger = logging.getLogger(__name__)

circle_client = CircleAPI(
    settings.CIRCLE_API_KEY,
    settings.CIRCLE_API_ENVIROMENT_URL)


@shared_task()
def check_payment_status():
    logger.debug("Payments checking...")
    for payment in CirclePayment.objects.filter(
            models.Q(status=CirclePayment.PENDING) | models.Q(status=CirclePayment.CONFIRMED)):
        logger.debug("Payment to check: %s", payment)
        with transaction.atomic():
            info_circle_reply = circle_client.payment_info(payment.id)
            payment.status = info_circle_reply['data']['status']

            if payment.status == CirclePayment.PAID:
                logger.debug("Payment has status PAID: %s", payment)
                payment.fee = Decimal(
                    info_circle_reply['data']['fees']['amount']).quantize(Decimal("0.01"))
                data = {
                    "idempotencyKey": str(uuid.uuid4()),
                    "source": {
                        "type": "wallet",
                        "id": "1000100943",
                    },
                    "destination": {
                        "type": "blockchain",
                        "address": payment.user.account.address,
                        "chain": "ALGO"
                    },
                    "amount": {
                        "amount": str(Decimal(payment.amount - payment.fee).quantize(Decimal("0.01"))),
                        "currency": "USD"
                    }
                }
                transfer_circle_reply = circle_client.transfer_usdc(data)
                CircleTransfer.objects.create(
                    id=transfer_circle_reply['data']['id'],
                    amount=transfer_circle_reply['data']['amount']['amount'],
                    user=payment.user,
                )

                payment.claimed = True

            payment.save()


@shared_task()
def check_transfer_status():
    logger.debug("Transfers checking...")
    for transfer in CircleTransfer.objects.filter(status=CircleTransfer.PENDING):
        with transaction.atomic():
            info_circle_reply = circle_client.transfer_info(transfer.id)
            transfer.status = info_circle_reply['data']['status']

            if transfer.status != CircleTransfer.PENDING:
                txn = Transaction.objects.create(
                    txid=info_circle_reply['data']['transactionHash'],
                    action=Transaction.TOP_UP,
                    currency=Transaction.USDC,
                    amount=info_circle_reply['data']['amount']['amount'],
                    to_account=transfer.user.account,
                    status=Transaction.CONFIRMED if transfer.status == CircleTransfer.COMPLETE else Transaction.REJECTED,
                )
                transfer.transaction = txn

            transfer.save()