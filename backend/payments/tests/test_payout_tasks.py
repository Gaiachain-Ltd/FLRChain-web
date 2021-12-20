from common.tests import CommonTestCase
from users.models import CustomUser
from accounts.models import Account
from payments.models import MTNPayout
from payments.tasks import process_payouts
from transactions.models import Transaction
from transactions.tasks import verify_transactions
from algorand import utils


class PayoutTasksTest(CommonTestCase):
    fixtures = ['main_account.json',]

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

    def test_process_payouts(self):
        payout = MTNPayout.payout(
            self.beneficiary, 
            0.01, 
            self.beneficiary.phone
        )

        process_payouts()

        payout.refresh_from_db()
        self.assertEqual(payout.status, MTNPayout.PENDING)
        self.assertEqual(payout.success, False)

        payout.success = True
        payout.save()

        txn = Transaction.transfer(
            self.main_account,
            self.beneficiary_account,
            0.01,
            Transaction.USDC,
            Transaction.FUELING
        )

        utils.wait_for_confirmation(txn.txid)

        process_payouts()

        payout.refresh_from_db()
        self.assertEqual(payout.status, MTNPayout.TRANSFERED)
        self.assertEqual(payout.success, True)

        utils.wait_for_confirmation(payout.transaction.txid)

        verify_transactions()
        process_payouts()
        
        payout.refresh_from_db()
        self.assertEqual(payout.status, MTNPayout.CONFIRMED)
        self.assertEqual(payout.success, True)

        process_payouts()
        
        payout.refresh_from_db()
        self.assertEqual(payout.status, MTNPayout.REQUESTED)
        self.assertEqual(payout.success, True)

        process_payouts()
        
        payout.refresh_from_db()
        self.assertEqual(payout.status, MTNPayout.COMPLETED)
        self.assertEqual(payout.success, True)


