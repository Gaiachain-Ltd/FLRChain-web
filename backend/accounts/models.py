from django.db import models, transaction
from algorand import utils
from django.conf import settings


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

    @staticmethod
    def get_main_account():
        return Account.objects.get(type=Account.MAIN_ACCOUNT)

    @staticmethod
    def generate(user):
        with transaction.atomic():
            private_key, address = utils.generate_account()

            created_account = Account.objects.create(
                user=user,
                private_key=private_key,
                address=address)

            #Opt-In:
            # main = Account.get_main_account()
            # utils.transfer_algos(
            #     main.address, 
            #     main.private_key,
            #     address,
            #     settings.ALGO_OPT_IN_AMOUNT)
            # TODO: Should we wait?
            return created_account

    def balance(self):
        return utils.check_balance(self.address)