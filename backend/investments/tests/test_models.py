from common.tests import CommonTestCase
from users.models import CustomUser
from accounts.models import Account
from projects.models import Project
from algorand import utils
from investments.models import Investment


class InvestmentModelTest(CommonTestCase):
    fixtures = ['main_account.json', ]

    def setUp(self):
        self.facililator = CustomUser.objects.create(
            email="facililator@test.com",
            first_name="facililator",
            last_name="facililator",
            type=CustomUser.FACILITATOR)

        self.facililator_account = Account.generate(self.facililator)

        self.investor = CustomUser.objects.create(
            email="investor@test.com",
            first_name="investor",
            last_name="investor",
            type=CustomUser.INVESTOR)

        self.investor_account = Account.generate(self.investor)

        self.project = Project.objects.create(
            owner=self.facililator,
            start="2020-03-01",
            end="2021-03-01",
            title="Ma project",
            description="Test")

    def test_finish(self):
        self.investment = Investment.objects.create(
            investor=self.investor,
            project=self.project,
            start="2020-03-01",
            end="2020-03-01",
            amount="0.0001")
        self.investment.refresh_from_db()
        txids, _ = SmartContract.generate(self.investment)
        for txid in txids:
            self.assertTrue(utils.wait_for_confirmation(txid))

        self.investment.refresh_from_db()
        txids = self.investment.finish()

        for txid in txids:
            self.assertTrue(utils.wait_for_confirmation(txid))

        self.investment.refresh_from_db()
        self.assertEqual(self.investment.status, Investment.FINISHED)