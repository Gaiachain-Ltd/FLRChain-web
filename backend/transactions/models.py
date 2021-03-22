from django.db import models
from django.conf import settings
from algorand import utils


class Transaction(models.Model):
    OPT_IN = 0
    ACTIONS = (
        (OPT_IN, "Opt-In action"),
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
    amount = models.PositiveIntegerField()
    fee = models.PositiveIntegerField() # Always in algos
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)

    @staticmethod
    def opt_in(to_account, from_account):
        # Opt-In Algos
        txid, fee = utils.transfer_algos(
            from_account.address, 
            from_account.private_key,
            to_account.address,
            settings.ALGO_OPT_IN_AMOUNT)

        Transaction.objects.create(
            txid=txid,
            from_user=from_account.user,
            to_user=to_account.user,
            from_address=from_account.address,
            to_address=to_account.address,
            action=Transaction.OPT_IN,
            currency=Transaction.ALGO,
            amount=settings.ALGO_OPT_IN_AMOUNT,
            fee=fee)

        # Opt-In USDC
        atxid, fee = utils.transfer_assets(
            from_account.address,
            from_account.private_key,
            to_account.address,
            0)

        Transaction.objects.create(
            txid=atxid,
            from_user=from_account.user,
            to_user=to_account.user,
            from_address=from_account.address,
            to_address=to_account.address,
            action=Transaction.OPT_IN,
            currency=Transaction.USDC,
            amount=0,
            fee=fee)
