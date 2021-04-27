from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser

client = APIClient()

class CommonTestCase(TestCase):

    def tearDown(self):
        from accounts.tasks import transfer_back_funds
        CustomUser.objects.all().delete()
        transfer_back_funds()

    def _auth(self, user):
        client.force_authenticate(user=user)

    def _create(self, user, url, data, status):
        self._auth(user)
        reply = client.post(url, data, format='json')
        self.assertEqual(reply.status_code, status)

    def _update(self, user, url, data, status):
        self._auth(user)
        reply = client.put(url, data, format='json')
        self.assertEqual(reply.status_code, status)

    def _list(self, user, url, status):
        self._auth(user)
        reply = client.get(url, format='json')
        self.assertEqual(reply.status_code, status)

    def _retrieve(self, user, url, status):
        self._auth(user)
        reply = client.get(url, format='json')
        self.assertEqual(reply.status_code, status)

