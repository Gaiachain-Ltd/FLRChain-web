import uuid
import logging
from django.db import models
from transactions.models import Transaction
from accounts.models import Account
from payments.mtn import MTNAPI
from django.conf import settings


logger = logging.getLogger(__name__)


mtn_client = MTNAPI(
    settings.MTN_SUBSCRIPTION_KEY,
    settings.MTN_API_KEY,
    settings.MTN_USER_ID,
    settings.MTN_URL,
    settings.MTN_CALLBACK_HOST
)


class CirclePayment(models.Model):
    FAILED = 'failed'
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PAID = 'paid'

    STATUS = (
        (FAILED, "Failed"),
        (PENDING, "Peding"),
        (CONFIRMED, "Confirmed"),
        (PAID, "Paid")
    )

    id = models.CharField(max_length=255, primary_key=True, editable=False)
    amount = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    fee = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING)
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.SET_NULL, null=True)
    claimed = models.BooleanField(default=False)


class CircleTransfer(models.Model):
    FAILED = 'failed'
    PENDING = 'pending'
    COMPLETE = 'complete'

    STATUS = (
        (FAILED, "Failed"),
        (PENDING, "Pending"),
        (COMPLETE, "Complete")
    )

    id = models.CharField(max_length=255, primary_key=True, editable=False)
    amount = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING)
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.SET_NULL, null=True)
    transaction = models.OneToOneField(
        'transactions.Transaction', on_delete=models.SET_NULL, null=True)


class MTNPayout(models.Model):
    """
    1. Wait for celery.
    2. Transfer USDC.
    3. Wait for confirmation.
    4. Transfer MOMO.
    5. Wait for confirmation.
    """
    PENDING = 0
    TRANSFERED = 1
    CONFIRMED = 2
    REQUESTED = 3
    COMPLETED = 4

    STATUS = (
        (PENDING, "Pending"),
        (TRANSFERED, "Transfered (USDC)"),
        (CONFIRMED, "Confirmed (USDC)"),
        (REQUESTED, "Requested (MTN)"),
        (COMPLETED, "Completed (MTN)")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    fee = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=PENDING)
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.SET_NULL, null=True)
    transaction = models.OneToOneField(
        'transactions.Transaction', on_delete=models.SET_NULL, null=True)
    success = models.NullBooleanField(default=None)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=16)

    def transfer(self):
        usdc_balance = self.user.account.usdc_balance()
        if usdc_balance < self.amount:
            logger.warning(f"Insufficient funds: {self.amount}/{usdc_balance}")
            self.success = False
        else:
            self.transaction = Transaction.transfer(
                self.user.account, 
                Account.get_main_account(),
                self.amount,
                Transaction.USDC,
                Transaction.PAYOUT
            )
            self.status = MTNPayout.TRANSFERED
            self.success = True

        self.save()

    def confirm(self):
        if self.transaction.status == Transaction.REJECTED:
            self.success = False
        elif self.transaction.status == Transaction.PENDING:
            self.success = None
        else:
            self.status = MTNPayout.CONFIRMED
            self.success = True

        self.save()

    def request(self):
        reply = mtn_client.transfer(
            str(self.amount), 
            self.phone,
            str(self.id)
        )
        if reply.status_code != 202:
            logger.error(f"Unable to transfer MOMO: {reply.status_code}/{reply.text}")
            self.success = False
        else:
            self.success = True
        
        self.status = MTNPayout.REQUESTED
        self.save()

    def complete(self):
        reply = mtn_client.get_transfer_status(str(self.id))
        if reply.status_code != 200:
            logger.error(f"Unable to check transfer's status: {reply.status_code}/{reply.text}")
            self.success = False
        elif reply.json()["status"] == "SUCCESSFUL":
            self.status = MTNPayout.COMPLETED
            self.success = True
        else:
            logger.debug(f"Transfer status: {reply.json()}")

        self.save()

    @staticmethod
    def payout(user, amount, phone):
        return MTNPayout.objects.create(
            amount=amount,
            user=user,
            phone=phone,
        )