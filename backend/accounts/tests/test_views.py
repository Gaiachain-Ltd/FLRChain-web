from common.tests import CommonTestCase
from users.models import CustomUser
from accounts.models import Account
from rest_framework import status
from projects.models import Project
from investments.models import Investment
from smart_contracts.models import SmartContract
from algorand import utils


class AccountsViewTest(CommonTestCase):
    fixtures = ['main_account.json', ]

    def setUp(self):
        self.beneficiary = CustomUser.objects.create(
            email="beneficiary@test.com",
            first_name="beneficiary",
            last_name="beneficiaryt",
            type=CustomUser.BENEFICIARY)

        self.beneficiary_account = Account.generate(self.beneficiary)

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

    def test_list(self):
        self._list(
            self.beneficiary, 
            "/api/v1/accounts/", 
            status.HTTP_200_OK)
        self._list(
            self.facililator, 
            "/api/v1/accounts/", 
            status.HTTP_200_OK)
        self._list(
            self.investor, 
            "/api/v1/accounts/", 
            status.HTTP_200_OK)

    def test_retrieve(self):
        self.investment = Investment.objects.create(
            investor=self.investor,
            project=self.project,
            start="2020-03-01",
            end="2020-03-01",
            amount="0.1")

        self.investment.refresh_from_db()

        txids, _ = SmartContract.generate(self.investment)
        for txid in txids:
            self.assertTrue(utils.wait_for_confirmation(txid))

        self._retrieve(
            self.beneficiary, 
            f"/api/v1/projects/{self.project.id}/accounts/", 
            status.HTTP_200_OK)
        self._retrieve(
            self.facililator, 
            f"/api/v1/projects/{self.project.id}/accounts/", 
            status.HTTP_200_OK)
        self._retrieve(
            self.investor, 
            f"/api/v1/projects/{self.project.id}/accounts/", 
            status.HTTP_200_OK)