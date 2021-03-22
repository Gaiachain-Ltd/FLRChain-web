from django.core.management.base import BaseCommand, CommandError
from accounts.models import Account
from users.models import CustomUser
from transactions.models import Transaction


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('investor_id', type=int)

    def handle(self, *args, **options):
        investor = CustomUser.objects.get(id=options['investor_id'])

        main_account = Account.get_main_account()
        investor_account = investor.account

        Transaction.transfer(
            main_account, 
            investor_account,
            1000,
            action=Transaction.FUELING)

        Transaction.transfer(
            main_account,
            investor_account,
            1000000,
            currency=Transaction.USDC,
            action=Transaction.FUELING)
