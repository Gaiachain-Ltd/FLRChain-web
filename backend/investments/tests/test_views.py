from common.tests import CommonTestCase
from rest_framework import status
from users.models import CustomUser
from accounts.models import Account
from projects.models import Project
from investments.models import Investment
from transactions.models import Transaction


class InvestmentsViewTest(CommonTestCase):
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

    def test_create(self):
        self._create(
            self.facililator, 
            f"/api/v1/projects/{self.project.id}/investments/", 
            {
                "start": "2020-03-01",
                "end": "2021-03-01",
                "amount": "0.01"
            }, status.HTTP_403_FORBIDDEN)

        self._create(
            self.investor, 
            f"/api/v1/projects/{self.project.id}/investments/", 
            {
                "start": "2020-03-01",
                "end": "2021-03-01",
                "amount": "0.01"
            }, status.HTTP_403_FORBIDDEN)

        Transaction.objects.all().update(status=Transaction.CONFIRMED)

        self._create(
            self.investor, 
            f"/api/v1/projects/{self.project.id}/investments/", 
            {
                "start": "2020-03-01",
                "end": "2021-03-01",
                "amount": "0.01"
            }, status.HTTP_201_CREATED)

    def test_retrieve(self):
        self.investment = Investment.objects.create(
            investor=self.investor,
            project=self.project,
            start="2020-03-01",
            end="2020-03-01",
            amount="0.0001")

        self._retrieve(
            self.facililator, 
            f"/api/v1/projects/{self.project.id}/investments/",
            status.HTTP_403_FORBIDDEN)

        self._retrieve(
            self.investor, 
            f"/api/v1/projects/{self.project.id}/investments/",
            status.HTTP_403_FORBIDDEN)

        Transaction.objects.all().update(status=Transaction.CONFIRMED)

        self._retrieve(
            self.investor, 
            f"/api/v1/projects/{self.project.id}/investments/",
            status.HTTP_200_OK)
            