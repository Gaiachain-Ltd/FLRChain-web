from users.models import CustomUser, Organization
from rest_framework import status
from common.tests import CommonTestCase


class OrganizationViewTest(CommonTestCase):
    fixtures = ['main_account.json', ]

    def setUp(self):
        self.user = CustomUser.objects.create(
            email="test@test.com",
            first_name="Test",
            last_name="Test"
        )
        
    def test_patrial_update(self):
        reply = self._patrial_update(
            self.user,
            "/api/v1/organization/",
            {
                "name": "TEST",
                "organization_type": 1,
                "website": "https://flrchain.milosolutions.com",
                "statement": "STATEMENT",
                "principal": "TEST",
                "email": "test@test.com",
                "phone": "111111"
            },
            status.HTTP_200_OK
        )

        self.assertEqual(reply.data["name"], "TEST")
        self.assertEqual(reply.data["organization_type"], 1)
        self.assertEqual(reply.data["website"], "https://flrchain.milosolutions.com")
        self.assertEqual(reply.data["statement"], "STATEMENT")
        self.assertEqual(reply.data["principal"], "TEST")
        self.assertEqual(reply.data["email"], "test@test.com")
        self.assertEqual(reply.data["phone"], "111111")

    def test_list(self):
        Organization.objects.create(
            user=self.user,
            name="TEST",
            statement="STATEMENT"
        )

        reply = self._list(
            self.user, 
            "/api/v1/organization/",
            status.HTTP_200_OK
        )

        self.assertEqual(reply.data["name"], "TEST")
        self.assertEqual(reply.data["organization_type"], None)
        self.assertEqual(reply.data["website"], None)
        self.assertEqual(reply.data["statement"], "STATEMENT")
        self.assertEqual(reply.data["principal"], None)
        self.assertEqual(reply.data["email"], None)
        self.assertEqual(reply.data["phone"], None)
