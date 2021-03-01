from django.db import models, transaction
from algorand import utils


class Account(models.Model):
    NORMAL_ACCOUNT = 0
    MASTER_ACCOUNT = 1
    ACCOUNT_TYPES = (
        (NORMAL_ACCOUNT, "Normal account"),
        (MASTER_ACCOUNT, "Master account") # TODO: Add constraint to keep single master account.
    )

    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, null=True)
    private_key = models.CharField(max_length=128)
    address = models.CharField(max_length=58)
    type = models.PositiveSmallIntegerField(default=NORMAL_ACCOUNT, choices=ACCOUNT_TYPES)

    @staticmethod
    def get_master_account():
        return Account.objects.get(type=Account.MASTER_ACCOUNT)

    @staticmethod
    def generate(user):
        with transaction.atomic():
            private_key, address = utils.generate_account()

            created_account = Account.objects.create(
                user=user,
                private_key=private_key,
                address=address)
            return created_account

    def balance(self):
        return utils.check_balance(self.address)