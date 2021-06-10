from common.tests import CommonTestCase
from users.models import CustomUser
from accounts.models import Account
from unittest.mock import Mock, patch
from payments.models import CirclePayment, CircleTransfer
from payments.tasks import check_payment_status, check_transfer_status
from transactions.models import Transaction


class PaymentTasksTest(CommonTestCase):
    fixtures = ['main_account.json', ]

    def setUp(self):
        self.investor = CustomUser.objects.create(
            email="investor@test.com",
            first_name="investor",
            last_name="investor",
            type=CustomUser.INVESTOR)

        self.investor_account = Account.generate(self.investor)

    def test_check_payment_status(self):
        cp = CirclePayment.objects.create(
            id='test',
            amount=11.99,
            fee=1.02,
            status=CirclePayment.PENDING,
            user=self.investor
        )

        with patch('payments.circle.CircleAPI.payment_info') as mock_payment_info:
            mock_payment_info.return_value = {'data': {'status': 'confirmed'}}
            check_payment_status()
            cp.refresh_from_db()
            self.assertEqual(cp.status, CirclePayment.CONFIRMED)

        with patch('payments.circle.CircleAPI.payment_info') as mock_payment_info, \
                patch('payments.circle.CircleAPI.transfer_usdc') as mock_transfer_usdc:
            mock_payment_info.return_value = {
                'data': {'status': 'paid', 'fees': {'amount': "1.02"}}}
            mock_transfer_usdc.return_value = {
                'data': {'id': 'transfer', 'amount': {'amount': "10.97"}}}
            check_payment_status()
            cp.refresh_from_db()
            self.assertEqual(cp.status, CirclePayment.PAID)
            self.assertEqual(CircleTransfer.objects.count(), 1)

    def test_check_transfer_status(self):
        ct = CircleTransfer.objects.create(
            id='1234',
            amount=10.22,
            status=CircleTransfer.PENDING,
            user=self.investor
        )

        with patch('payments.circle.CircleAPI.transfer_info') as mock_transfer_info:
            mock_transfer_info.return_value = {'data': {
                'status': 'complete', 'transactionHash': '1222', 'amount': {'amount': "10.22"}}}
            check_transfer_status()
            ct.refresh_from_db()
            self.assertEqual(ct.status, CircleTransfer.COMPLETE)
            self.assertEqual(
                Transaction.objects.filter(action=Transaction.TOP_UP).count(), 1)