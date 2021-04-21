from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from rest_framework import status
from projects.models import Project

client = APIClient()


class ProjectsViewTest(TestCase):
    fixtures = ['main_account.json', ]

    def setUp(self):
        self.user = CustomUser.objects.create(
            email="test@test.com",
            first_name="Test",
            last_name="Test",
            type=CustomUser.FACILITATOR)

        self.project = Project.objects.create(
            owner=self.user,
            start="2020-03-01",
            end="2021-03-01",
            title="Ma project",
            description="Test")

    def test_list(self):
        def _list(status):
            reply = client.get('/api/v1/projects/', format='json')
            self.assertEqual(reply.status_code, status)
            return reply

        client.force_authenticate(user=self.user)
        _list(status.HTTP_200_OK)

    def test_create(self):
        def _create(data, status):
            reply = client.post('/api/v1/projects/', data, format='json')
            self.assertEqual(reply.status_code, status)

        client.force_authenticate(user=self.user)

        _create({
                'start': "2020-03-01",
                'end': "2021-03-01",
                'title': "My project",
                'description': "Test",
                'tasks': []
                }, status.HTTP_201_CREATED)

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