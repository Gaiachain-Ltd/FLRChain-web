from common.tests import CommonTestCase
from users.models import CustomUser
from accounts.models import Account
from projects.models import Project
from investments.models import Investment
from smart_contracts.models import SmartContract
from transactions.models import Transaction
from algorand import utils


class SmartContractModelTest(CommonTestCase):
    fixtures = ['main_account.json', ]

    def setUp(self):
        self.beneficiary = CustomUser.objects.create(
            email="beneficiary@test.com",
            first_name="beneficiary",
            last_name="beneficiaryt",
            type=CustomUser.BENEFICIARY)

        self.facililator = CustomUser.objects.create(
            email="facililator@test.com",
            first_name="facililator",
            last_name="facililator",
            type=CustomUser.FACILITATOR)

        self.investor = CustomUser.objects.create(
            email="investor@test.com",
            first_name="investor",
            last_name="investor",
            type=CustomUser.INVESTOR)

        self.beneficiary_account = Account.generate(self.beneficiary)
        self.facililator_account = Account.generate(self.facililator)
        self.investor_account = Account.generate(self.investor)

        self.project = Project.objects.create(
            owner=self.facililator,
            start="2020-03-01",
            end="2021-03-01",
            title="Ma project",
            description="Test")

        self.investment = Investment.objects.create(
            investor=self.investor,
            project=self.project,
            status=Investment.INVESTED,
            start="2020-03-01",
            end="2021-03-01",
            amount="0.0001")

    def test_smart_contract(self):
        self.investment.refresh_from_db()
        txids, smart_contract_account = SmartContract.generate(self.investment)

        for txid in txids:
            print("INFO", utils.wait_for_confirmation(txid))

        txid = Transaction.transfer(
            smart_contract_account, 
            self.beneficiary_account, 
            0.00001, 
            Transaction.USDC, 
            Transaction.REWARD)

        print("INFO", utils.wait_for_confirmation(txid.txid))

        txid = Transaction.transfer(
            smart_contract_account, 
            self.facililator_account, 
            0.00001, 
            Transaction.USDC, 
            Transaction.TRANSFER)

        print("INFO", utils.wait_for_confirmation(txid.txid))

        txid = Transaction.transfer(
            smart_contract_account, 
            self.investor_account, 
            0.00001, 
            Transaction.USDC, 
            Transaction.CLOSE,
            self.investor_account)

        print("INFO", utils.wait_for_confirmation(txid.txid))


