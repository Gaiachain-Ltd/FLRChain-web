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
    ACCOUNT_TYPES = (
        (NORMAL_ACCOUNT, "Normal account"),
        (MAIN_ACCOUNT, "Main account") # TODO: Add constraint to keep single main account.
    )

    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, null=True)
    private_key = models.CharField(max_length=128)
    address = models.CharField(max_length=58)
    type = models.PositiveSmallIntegerField(default=NORMAL_ACCOUNT, choices=ACCOUNT_TYPES)
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

            main_account = Account.get_main_account()
            Transaction.opt_in(
                created_account, 
                main_account,
                True)
            logger.debug("Opt-In transaction for user %s account.", user)
            
            return created_account

    def balance(self):
        return utils.check_balance(self.address)