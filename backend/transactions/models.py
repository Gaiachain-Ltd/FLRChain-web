import logging
from django.db import models
from django.conf import settings
from algorand import utils


logger = logging.getLogger(__name__)


class Transaction(models.Model):
    OPT_IN = 0
    FUELING = 1
    TRANSFER = 2
    CLOSE = 3
    ACTIONS = (
        (OPT_IN, "Opt-In action"),
        (FUELING, "Fueling action"),
        (TRANSFER, "Transfer"),
        (CLOSE, "Close account")
    )

    ALGO = 0
    USDC = 1
    CURRENCIES = (
        (ALGO, "Algos"),
        (USDC, "USDC")
    )

    from_user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        related_name='sender')
    to_user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        related_name='receiver')
    from_address = models.CharField(max_length=58)
    to_address = models.CharField(max_length=58)
    txid = models.CharField(max_length=64)
    action = models.PositiveSmallIntegerField(choices=ACTIONS)
    currency = models.PositiveSmallIntegerField(choices=CURRENCIES)
    amount = models.BigIntegerField()
    fee = models.BigIntegerField()  # Always in algos
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)
    atomic = models.BooleanField(default=False)

    @staticmethod
    def opt_in(to_account, from_account, fuel):
        txns = list()

        # Opt-In Algos
        txns.append((Transaction.prepare_transfer(
            from_account,
            to_account,
            settings.ALGO_OPT_IN_AMOUNT,
            action=Transaction.OPT_IN)))

        # Opt-In USDC
        txns.append((Transaction.prepare_transfer(
            to_account,
            to_account,
            0,
            Transaction.USDC,
            Transaction.OPT_IN)))

        if fuel:
            logger.warning("Fueling investor account: %s", to_account.user)
            txns.append((Transaction.prepare_transfer(
                from_account,
                to_account,
                1000,
                action=Transaction.FUELING)))

            txns.append((Transaction.prepare_transfer(
                from_account,
                to_account,
                1000000,  # 1x USDC
                currency=Transaction.USDC,
                action=Transaction.FUELING)))

        txid = utils.atomic_transfer(txns)

        # TODO: batch_create
        for tx in txns:
            trans = tx[1]
            trans.txid = txid
            trans.save()

    @staticmethod
    def transfer(sender, receiver, amount,
                 currency=0, action=2, close=None):
        if currency == Transaction.ALGO:
            txid, fee = utils.transfer_algos(
                sender.address,
                sender.private_key,
                receiver.address,
                amount,
                close_remainder_to=close.address if close else None)
        else:
            txid, fee = utils.transfer_assets(
                sender.address,
                sender.private_key,
                receiver.address,
                amount,
                close_assets_to=close.address if close else None)

        Transaction.objects.create(
            txid=txid,
            from_user=sender.user,
            to_user=receiver.user,
            from_address=sender.address,
            to_address=receiver.address,
            action=action,
            currency=currency,
            amount=amount,
            fee=fee)

        logger.debug("Sent transaction %s, amount: %s, fee: %s",
                     txid, amount, fee)

    @staticmethod
    def prepare_transfer(sender, receiver, amount,
                         currency=0, action=2):
        if currency == Transaction.ALGO:
            txn, fee = utils.prepare_transfer_algos(
                sender.address,
                sender.private_key,
                receiver.address,
                amount)
        else:
            txn, fee = utils.prepare_transfer_assets(
                sender.address,
                sender.private_key,
                receiver.address,
                amount)

        logger.debug("Prepare transaction, amount: %s, fee: %s", amount, fee)

        return txn, Transaction(
            from_user=sender.user,
            to_user=receiver.user,
            from_address=sender.address,
            to_address=receiver.address,
            action=action,
            currency=currency,
            amount=amount,
            fee=fee,
            atomic=True)

    @staticmethod
    def close_account(sender, receiver):
        atxid, fee = utils.transfer_assets(
            sender.address,
            sender.private_key,
            receiver.address,
            0,
            close_assets_to=receiver.address)

        Transaction.objects.create(
            txid=atxid,
            from_user=None,
            to_user=receiver.user,
            from_address=sender.address,
            to_address=receiver.address,
            action=Transaction.CLOSE,
            currency=Transaction.USDC,
            amount=0,
            fee=fee)

        txid, fee = utils.transfer_algos(
            sender.address,
            sender.private_key,
            receiver.address,
            0,
            receiver.address)
            
        Transaction.objects.create(
            txid=txid,
            from_user=None,
            to_user=receiver.user,
            from_address=sender.address,
            to_address=receiver.address,
            action=Transaction.CLOSE,
            currency=Transaction.ALGO,
            amount=0,
            fee=fee)
