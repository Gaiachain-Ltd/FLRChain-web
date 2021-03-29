import logging
from django.db import models, transaction
from algorand import utils
from django.conf import settings
from transactions.models import Transaction
from users.models import CustomUser


logger = logging.getLogger(__name__)


class Account(models.Model):
    NORMAL_ACCOUNT = 0
    MAIN_ACCOUNT = 1
    SMART_CONTRACT_ACCOUNT = 2
    ACCOUNT_TYPES = (
        (NORMAL_ACCOUNT, "Normal account"),
        # TODO: Add constraint to keep single main account.
        (MAIN_ACCOUNT, "Main account"),
        (SMART_CONTRACT_ACCOUNT, "Smart contract account")
    )

    user = models.OneToOneField(
        'users.CustomUser', on_delete=models.CASCADE, null=True)
    smart_contract = models.OneToOneField(
        'smart_contracts.SmartContract', on_delete=models.CASCADE, 
        null=True, blank=True)
    private_key = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=58)
    type = models.PositiveSmallIntegerField(
        default=NORMAL_ACCOUNT, choices=ACCOUNT_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_main_account():
        return Account.objects.get(type=Account.MAIN_ACCOUNT)

    @staticmethod
    def generate(user):
        with transaction.atomic():
            private_key, address = utils.generate_account()
            logger.debug("Generated algorand account for user %s.", user)

            created_account = Account.objects.create(
                user=user,
                private_key=private_key,
                address=address)
            logger.debug("Created account for user %s.", user)

            # ONLY FOR TEST PURPOSES!!
            if user.type == CustomUser.INVESTOR:
                main_account = Account.get_main_account()
                chained = [
                    Transaction.prepare_transfer(
                        main_account,
                        created_account,
                        0.01,
                        action=Transaction.FUELING),
                    Transaction.prepare_transfer(
                        main_account,
                        created_account,
                        1,
                        currency=Transaction.USDC,
                        action=Transaction.FUELING)]
            else:
                chained = []

            created_account.opt_in(chained)
            return created_account

    def opt_in(self, chain=[]):
        main_account = Account.get_main_account()
        Transaction.opt_in(
            self,
            main_account,
            chain)
        logger.debug("Opt-In transaction for %s account.", self.address)

    def usdc_balance(self):
        return utils.usdc_balance(self.address)
