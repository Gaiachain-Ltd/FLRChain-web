from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from rest_framework import status
from projects.models import Project

client = APIClient()


class ProjectsViewTest(TestCase):
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

        self.project = Project.objects.create(
            owner=self.facililator,
            start="2020-03-01",
            end="2021-03-01",
            title="Ma project",
            description="Test")

    def test_list(self):
        def _list(status):
            reply = client.get('/api/v1/projects/', format='json')
            self.assertEqual(reply.status_code, status)
            return reply

        client.force_authenticate(user=self.facililator)
        _list(status.HTTP_200_OK)

    def test_create(self):
        def _create(data, status):
            reply = client.post('/api/v1/projects/', data, format='json')
            self.assertEqual(reply.status_code, status)

        for data in [
            (self.beneficiary, status.HTTP_403_FORBIDDEN),
            (self.facililator, status.HTTP_201_CREATED),
            (self.investor, status.HTTP_403_FORBIDDEN)]:
            client.force_authenticate(user=data[0])

            _create({
                    'start': "2020-03-01",
                    'end': "2021-03-01",
                    'title': "My project",
                    'description': "Test",
                    'tasks': []
                    }, data[1])

        client.force_authenticate(user=self.facililator)

        # Incorrect start/end:
        #TODO: Handle it!
        _create({
                'start': "2021-03-01",
                'end': "2020-03-01",
                'title': "My project",
                'description': "Test",
                'tasks': []
                }, status.HTTP_201_CREATED)

        # Tasks:
        _create({
            'start': "2021-03-01",
            'end': "2020-03-01",
            'title': "My project",
            'description': "Test",
            'tasks': [{
                'action': "Task!",
                'reward': 0.0001
            }]
        }, status.HTTP_201_CREATED)

    def test_retrieve(self):
        def _retrieve(status):
            reply = client.get(f'/api/v1/project/{self.project.id}/')
            self.assertEqual(reply.status_code, status)

        