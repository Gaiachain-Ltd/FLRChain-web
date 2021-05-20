from unittest.mock import Mock, patch
from common.tests import CommonTestCase
from users.models import CustomUser
from accounts.models import Account
from transactions.models import Transaction
from algorand import utils
from transactions.tasks import verify_transactions


class TransactionTasksTest(CommonTestCase):
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

    def test_confirmed(self):
        main_account = Account.get_main_account()
        tx = Transaction.transfer(
            main_account,
            self.user_account,
            0.1,
            Transaction.ALGO,
            Transaction.OPT_IN)
        self.assertTrue(utils.wait_for_confirmation(tx.txid))
        verify_transactions()
        tx.refresh_from_db()
        self.assertEqual(tx.status, Transaction.CONFIRMED)

    def test_rejected_pool_error(self):
        main_account = Account.get_main_account()
        with patch('algorand.utils.transaction_info') as mock_transaction_info:
            mock_transaction_info.return_value = {'pool-error': 'error'}
            tx = Transaction.transfer(
                main_account,
                self.user_account,
                0.1,
                Transaction.ALGO,
                Transaction.OPT_IN)
            self.assertTrue(utils.wait_for_confirmation(tx.txid))
            verify_transactions()
            tx.refresh_from_db()
            self.assertEqual(tx.status, Transaction.REJECTED)
            self.assertEqual(Transaction.objects.count(), 2)

    def test_rejected_expired(self):
        main_account = Account.get_main_account()
        with patch('algorand.utils.transaction_info') as mock_transaction_info:
            mock_transaction_info.return_value = {
                'pool-error': '', 'txn': {'txn': {'lv': utils.status()['last-round']-1000}}}
            tx = Transaction.transfer(
                main_account,
                self.user_account,
                0.1,
                Transaction.ALGO,
                Transaction.OPT_IN)
            self.assertTrue(utils.wait_for_confirmation(tx.txid))
            verify_transactions()
            tx.refresh_from_db()
            self.assertEqual(tx.status, Transaction.REJECTED)
            self.assertEqual(Transaction.objects.count(), 2)

    def test_rejected_atomic(self):
        main_account = Account.get_main_account()
        with patch('algorand.utils.transaction_info') as mock_transaction_info:
            mock_transaction_info.return_value = {
                'pool-error': '', 'txn': {'txn': {'lv': utils.status()['last-round']-1000}}}
            tx0 = Transaction.prepare_transfer(
                main_account,
                self.user_account,
                0.21,
                Transaction.ALGO,
                Transaction.OPT_IN)
            tx1 = Transaction.prepare_transfer(
                self.user_account,
                self.user_account,
                0,
                Transaction.USDC,
                Transaction.OPT_IN)
            tx2 = Transaction.prepare_transfer(
                main_account,
                self.user_account,
                0.1,
                Transaction.USDC,
                Transaction.OPT_IN)
            txids = Transaction.atomic_transfer([tx0, tx1, tx2])
            for txid in txids:
                self.assertTrue(utils.wait_for_confirmation(txid))

            verify_transactions()

            self.assertEqual(Transaction.objects.filter(status=Transaction.REJECTED).count(), 3)
            self.assertEqual(Transaction.objects.count(), 6)

            one_without_prev = False
            for txn in Transaction.objects.filter(retries=1):
                if not one_without_prev and txn.atomic_prev is None:
                    one_without_prev = True
                    continue
                
                self.assertFalse(txn.atomic_prev is None)