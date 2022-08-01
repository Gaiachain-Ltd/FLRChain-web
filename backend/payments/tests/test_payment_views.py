from common.tests import CommonTestCase
from users.models import CustomUser
from accounts.models import Account
from rest_framework import status
from unittest.mock import Mock, patch


class CirclePaymentViewTest(CommonTestCase):
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

        self.investor_account = Account.generate(self.investor)

    def test_get_key(self):
        self._list(
            self.beneficiary,
            "/api/v1/payments/circle/key/",
            status.HTTP_403_FORBIDDEN)

        self._list(
            self.facililator,
            "/api/v1/payments/circle/key/",
            status.HTTP_403_FORBIDDEN)

        with patch('payments.circle.CircleAPI.get_public_key') as mock_get_public_key:
            mock_get_public_key.return_value = {'data': {'test': "Test"}}
            reply = self._list(
                self.investor,
                "/api/v1/payments/circle/key/",
                status.HTTP_200_OK)

            self.assertEqual(
                reply.data, mock_get_public_key.return_value['data'])

    def test_save_card(self):
        data = {
            "idempotencyKey": "test",
            "keyId": "1234",
            "expiry": "12/1333",
            "encryptedData": "Test",
            "billingDetails": {
                "name": "Test Test",
                "city": "Lublin",
                "country": "PL",
                "address": "Test",
                "postalCode": "122-111",
                "district": ""
            }
        }

        self._create(
            self.beneficiary, 
            "/api/v1/payments/circle/card/",
            data, status.HTTP_403_FORBIDDEN)

        self._create(
            self.facililator, 
            "/api/v1/payments/circle/card/",
            data, status.HTTP_403_FORBIDDEN)

        with patch('payments.circle.CircleAPI.save_card') as mock_save_card:
            mock_save_card.return_value = {'test': "Test"}
            reply = self._create(
                self.investor, 
                "/api/v1/payments/circle/card/",
                data, status.HTTP_200_OK)
            self.assertEqual(reply.data, mock_save_card.return_value)

    def test_make_payment(self):
        data = {
            "idempotencyKey": "test",
            "keyId": "1234",
            "amount": 11.99,
            "cardId": "12334",
            "encryptedData": "Test"
        }

        self._create(
            self.beneficiary, 
            "/api/v1/payments/circle/card/payment/",
            data, status.HTTP_403_FORBIDDEN)

        self._create(
            self.facililator, 
            "/api/v1/payments/circle/card/payment/",
            data, status.HTTP_403_FORBIDDEN)

        with patch('payments.circle.CircleAPI.create_payment') as mock_make_payment:
            mock_make_payment.return_value = {'data': {'id': "Test", 'amount': {'amount': 11.99}}}
            reply = self._create(
                self.investor, 
                "/api/v1/payments/circle/card/payment/",
                data, status.HTTP_200_OK)
            self.assertEqual(reply.data, mock_make_payment.return_value)