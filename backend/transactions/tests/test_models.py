from common.tests import CommonTestCase
from users.models import CustomUser
from accounts.models import Account
from transactions.models import Transaction
from algorand import utils


class TransactionModelTest(CommonTestCase):
    fixtures = ['main_account.json', ]

    def setUp(self):
        self.user = CustomUser.objects.create(
            email="test@test.com",
            first_name="Test",
            last_name="Test",)

        private_key, address = utils.generate_account()
        self.user_account = Account.objects.create(
            user=self.user,
            private_key=private_key,
            address=address,
            type=Account.NORMAL_ACCOUNT)

    def test_opt_in(self):
        main_account = Account.get_main_account()
        txids = Transaction.opt_in(self.user_account, main_account)
        for txid in txids:
            # TODO:
            print("INFO", utils.wait_for_confirmation(txid))

    def test_opt_in_chain(self):
        main_account = Account.get_main_account()
        txids = Transaction.opt_in(
            self.user_account, 
            main_account,
            [
                Transaction.prepare_transfer(
                main_account,
                self.user_account,
                0.0001,
                Transaction.USDC,
                Transaction.FUELING),
            ])

        for txid in txids:
            # TODO:
            print("INFO", utils.wait_for_confirmation(txid))

    def test_transfer(self):
        main_account = Account.get_main_account()
        txid = Transaction.transfer(main_account, self.user_account, 0.1, Transaction.ALGO, Transaction.OPT_IN)
        # TODO:
        print("INFO", utils.wait_for_confirmation(txid.txid))