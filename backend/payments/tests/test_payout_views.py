from common.tests import CommonTestCase
from users.models import CustomUser
from accounts.models import Account
from rest_framework import status
from transactions.models import Transaction
from algorand import utils


class CirclePaymentViewTest(CommonTestCase):
    fixtures = ['main_account.json', ]

    def setUp(self):
        self.beneficiary = CustomUser.objects.create(
            email="beneficiary@flrchain.com",
            first_name="beneficiary",
            last_name="beneficiary",
            phone="46000000000",
            type=CustomUser.BENEFICIARY
        )

        self.beneficiary_account = Account.generate(self.beneficiary)

        self.main_account = Account.get_main_account()

    def test_payout_failure(self):
        reply = self._create(
            self.beneficiary,
            "/api/v1/payments/mtn/payout/",
            {
                "amount": "10.00"
            },
            status.HTTP_200_OK
        )
        self.assertEqual(reply.data['success'], False)

    def test_payout_failure(self):
        txn = Transaction.transfer(
            self.main_account,
            self.beneficiary_account,
            0.01,
            Transaction.USDC,
            Transaction.FUELING
        )

        utils.wait_for_confirmation(txn.txid)

        reply = self._create(
            self.beneficiary,
            "/api/v1/payments/mtn/payout/",
            {
                "amount": "0.01",
                "phone": self.beneficiary.phone,
            },
            status.HTTP_200_OK
        )
        self.assertEqual(reply.data['success'], True)