from django.test import TestCase
from users.models import CustomUser
from projects.serializers import ProjectSerializer


class ProjectSerializerTest(TestCase):
    def test_validate(self):
        serializer = ProjectSerializer(data={
            'start': "2022-03-01",
            'end': "2021-03-01",
            'title': "My project",
            'description': "Test",
            'tasks': []
        })
        self.assertEqual(serializer.is_valid(), False)

        serializer = ProjectSerializer(data={
            'start': "2019-03-01",
            'end': "2021-03-01",
            'title': "My project",
            'description': "Test",
            'tasks': []
        })
        self.assertEqual(serializer.is_valid(), True)