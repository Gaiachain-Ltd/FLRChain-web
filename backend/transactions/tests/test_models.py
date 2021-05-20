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
            self.assertTrue(utils.wait_for_confirmation(txid))

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
            self.assertTrue(utils.wait_for_confirmation(txid))

    def test_transfer(self):
        main_account = Account.get_main_account()
        txid = Transaction.transfer(main_account, self.user_account, 0.1, Transaction.ALGO, Transaction.OPT_IN)
        self.assertTrue(utils.wait_for_confirmation(txid.txid))

    def test_retry_single(self):
        main_account = Account.get_main_account()
        txn = Transaction.objects.create(
            from_account=main_account,
            to_account=self.user_account,
            amount=0.1,
            currency=Transaction.ALGO,
            action=Transaction.FUELING,
            retries=3)
        
        with self.assertRaises(Exception):
            txn.retry()

        txn.retries = 0
        txn.save()

        with self.assertRaises(Exception):
            txn.retry()

        txn.status = Transaction.REJECTED
        txid = txn.retry()
        self.assertTrue(utils.wait_for_confirmation(txid))

    
    def test_retry_atomic(self):
        main_account = Account.get_main_account()
        txn0 = Transaction.objects.create(
            from_account=main_account,
            to_account=self.user_account,
            amount=0.21,
            currency=Transaction.ALGO,
            action=Transaction.OPT_IN,
            status=Transaction.REJECTED,
            atomic=True,)
        txn1 = Transaction.objects.create(
            from_account=self.user_account,
            to_account=self.user_account,
            amount=0,
            currency=Transaction.USDC,
            action=Transaction.OPT_IN,
            atomic=True,
            atomic_prev=txn0)
        txn2 = Transaction.objects.create(
            from_account=main_account,
            to_account=self.user_account,
            amount=0.1,
            currency=Transaction.USDC,
            action=Transaction.FUELING,
            atomic=True,
            atomic_prev=txn1)

        txids = txn0.retry()
        for txid in txids:
            self.assertTrue(utils.wait_for_confirmation(txid))

        self.assertEqual(Transaction.objects.count(), 6)