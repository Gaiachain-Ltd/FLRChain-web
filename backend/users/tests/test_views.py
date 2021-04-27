from users.models import CustomUser
from rest_framework import status
from common.tests import CommonTestCase


class UsersViewTest(CommonTestCase):
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
        self._create(
            None,
            '/api/v1/register/',
            {
                'email': 'test@test.com',
                'type': 1,
                'first_name': 'Test',
                'last_name': 'Test',
                'password': 'Test',
                'phone': '',
                'village': '',
            }, status.HTTP_400_BAD_REQUEST)

        self._create(
            None,
            '/api/v1/register/',
            {
                'email': 'test@test0.com',
                'type': 1,
                'first_name': 'Test',
                'last_name': 'Test',
                'password': 'Test',
            }, status.HTTP_201_CREATED)

        for acc_type in [1, 2, 3]:
            self._create(
                None,
                '/api/v1/register/',
                {
                    'email': f'test@test{acc_type}.com',
                    'type': acc_type,
                    'first_name': 'Test',
                    'last_name': 'Test',
                    'password': 'Test',
                    'phone': '',
                    'village': '',
                }, status.HTTP_201_CREATED)

    def test_login(self):
        self._create(
            None,
            '/api/v1/login/',
            {
                'username': 'test@test.com',
                'password': 'test'
            }, status.HTTP_400_BAD_REQUEST)

        self._create(
            None,
            '/api/v1/login/',
            {
                'username': 'test@test.com',
                'password': 'test12345'
            }, status.HTTP_200_OK)

    def test_info(self):
        self._list(self.user, '/api/v1/info/', status.HTTP_200_OK)
