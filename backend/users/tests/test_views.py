from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from rest_framework import status


client = APIClient()


class UsersViewTest(TestCase):
    fixtures = ['main_account.json', ]

    def setUp(self):
        self.user = CustomUser.objects.create(
            email="test@test.com",
            first_name="Test",
            last_name="Test")
        self.user.set_password('test12345')
        self.user.save()

    def tearDown(self):
        from accounts.tasks import transfer_back_funds

        CustomUser.objects.all().delete()
        transfer_back_funds()

    def test_register(self):
        def _register(data, status):
            reply = client.post(
                '/api/v1/register/',
                data,
                format='json')
            self.assertEqual(reply.status_code, status)

        _register({
            'email': 'test@test.com',
            'type': 1,
            'first_name': 'Test',
            'last_name': 'Test',
            'password': 'Test',
            'phone': '',
            'village': '',
        }, status.HTTP_400_BAD_REQUEST)

        _register({
            'email': 'test@test0.com',
            'type': 1,
            'first_name': 'Test',
            'last_name': 'Test',
            'password': 'Test',
        }, status.HTTP_201_CREATED)

        for acc_type in [1, 2, 3]:
            _register({
                'email': f'test@test{acc_type}.com',
                'type': acc_type,
                'first_name': 'Test',
                'last_name': 'Test',
                'password': 'Test',
                'phone': '',
                'village': '',
            }, status.HTTP_201_CREATED)

    def test_login(self):
        def _login(data, status):
            reply = client.post('/api/v1/login/', data, format='json')
            self.assertEqual(reply.status_code, status)

        _login({
            'username': 'test@test.com',
            'password': 'test'
        }, status.HTTP_400_BAD_REQUEST)

        _login({
            'username': 'test@test.com',
            'password': 'test12345'
        }, status.HTTP_200_OK)

    def test_inf(self):
        def _info(status):
            reply = client.get('/api/v1/info/', format='json')
            self.assertEqual(reply.status_code, status)

        client.force_authenticate(user=self.user)
        _info(status.HTTP_200_OK)
