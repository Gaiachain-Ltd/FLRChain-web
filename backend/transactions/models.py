import logging
from django.db import models
from django.conf import settings
from algorand import utils
from django.db import transaction


logger = logging.getLogger(__name__)


class Transaction(models.Model):
    OPT_IN = 0
    FUELING = 1
    TRANSFER = 2
    CLOSE = 3
    INVESTMENT = 4
    REWARD = 5
    FACILITATOR_FEE = 6
    RETURN_INVESTMENT = 7
    ACTIONS = (
        (OPT_IN, "Opt-In action"),
        (FUELING, "Fueling action"),
        (TRANSFER, "Transfer"),
        (CLOSE, "Close account"),
        (INVESTMENT, "Investment"),
        (REWARD, "Beneficiary reward"),
        (FACILITATOR_FEE, "Facilitator fee"),
        (RETURN_INVESTMENT, "Return investment")
    )

    ALGO = 0
    USDC = 1
    CURRENCIES = (
        (ALGO, "Algos"),
        (USDC, "USDC")
    )

    REJECTED = 0
    CONFIRMED = 1
    PENDING = 2
    STATUS = (
        (REJECTED, "Rejected"),
        (CONFIRMED, "Confirmed"),
        (PENDING, "Pending")
    )

    MAX_RETRIES = 3

    from_account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.SET_NULL,
        null=True,
        related_name='sender')
    to_account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.SET_NULL,
        null=True,
        related_name='receiver')
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True)
    txid = models.CharField(max_length=64)
    action = models.PositiveSmallIntegerField(choices=ACTIONS)
    currency = models.PositiveSmallIntegerField(choices=CURRENCIES)
    amount = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    fee = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)  # Always in algos
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=PENDING)
    retries = models.PositiveSmallIntegerField(default=0)
    repeated_for = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    
    def retry(self):
        if self.status != Transaction.REJECTED:
            raise Exception({"status": "Cannot retry non-rejected transaction."})

        if self.retries + 1 > Transaction.MAX_RETRIES:
            raise Exception({"retries": "Cannot retry this transaction."})
        
        t = None
        with transaction.atomic():
            t = Transaction.transfer(
                self.from_account,
                self.to_account,
                self.amount,
                self.currency,
                self.action,
                self.to_account if self.action == Transaction.CLOSE else None,
                self.project)

            t.retries = self.retries + 1
            t.repeated_for = self
            t.save()
        
        return t
        
    @staticmethod
    def opt_in(to_account, from_account, chain=[]):
        txns = list()

        # Opt-In Algos
        txns.append(Transaction.prepare_transfer(
            from_account,
            to_account,
            settings.ALGO_OPT_IN_AMOUNT,
            action=Transaction.OPT_IN))

        # Opt-In USDC
        txns.append(Transaction.prepare_transfer(
            to_account,
            to_account,
            0,
            Transaction.USDC,
            Transaction.OPT_IN))

        txns.extend(chain)
        utils.atomic_transfer(txns)

        # TODO: batch_create
        for tx in txns:
            trans = tx[1]
            trans.save()

        return [tx[1].txid for tx in txns]

    @staticmethod
    def transfer(sender, receiver, amount,
                 currency=0, action=2, close=None, 
                 project=None):
        if currency == Transaction.ALGO:
            txid, fee = utils.transfer_algos(
                sender,
                receiver,
                amount,
                close_remainder_to=close if close else None)
        else:
            txid, fee = utils.transfer_assets(
                sender,
                receiver,
                amount,
                close_assets_to=close if close else None)

        logger.debug("Sent transaction %s, amount: %s, fee: %s",
                     txid, amount, fee)

        return Transaction.objects.create(
            txid=txid,
            from_account=sender,
            to_account=receiver,
            action=action,
            currency=currency,
            amount=amount,
            fee=fee,
            project=project)

    @staticmethod
    def prepare_transfer(sender, receiver, amount,
                         currency=0, action=2, project=None):
        if currency == Transaction.ALGO:
            txn, fee = utils.prepare_transfer_algos(
                sender,
                receiver,
                amount)
        else:
            txn, fee = utils.prepare_transfer_assets(
                sender,
                receiver,
                amount)

        logger.debug("Prepare transaction, amount: %s, fee: %s", (amount * 1000000), fee)

        return (txn, Transaction(
            from_account=sender,
            to_account=receiver,
            action=action,
            currency=currency,
            amount=amount,
            fee=fee,
            project=project))

    @staticmethod
    def close_account(sender, receiver):
        atxid, fee = utils.transfer_assets(
            sender,
            receiver,
            0,
            close_assets_to=receiver)

        Transaction.objects.create(
            txid=atxid,
            from_account=None,
            to_account=receiver,
            action=Transaction.CLOSE,
            currency=Transaction.USDC,
            amount=0,
            fee=fee)

        txid, fee = utils.transfer_algos(
            sender,
            receiver,
            0,
            receiver)
            
        Transaction.objects.create(
            txid=txid,
            from_account=None,
            to_account=receiver,
            action=Transaction.CLOSE,
            currency=Transaction.ALGO,
            amount=0,
            fee=fee)
