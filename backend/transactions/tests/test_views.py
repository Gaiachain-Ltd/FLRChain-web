from common.tests import CommonTestCase
from rest_framework import status
from users.models import CustomUser
from accounts.models import Account


class TransactionsViewTest(CommonTestCase):
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

        self.facilitator_account = Account.generate(self.facililator)

        self.investor_account = Account.generate(self.investor)

    def test_list(self):
        self._list(
            self.beneficiary, 
            "/api/v1/transactions/", 
            status.HTTP_200_OK)
        self._list(
            self.facililator, 
            "/api/v1/transactions/", 
            status.HTTP_200_OK)
        self._list(
            self.investor, 
            "/api/v1/transactions/", 
            status.HTTP_200_OK)