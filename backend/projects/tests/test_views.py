from users.models import CustomUser
from rest_framework import status
from projects.models import Project, Assignment
from common.tests import CommonTestCase


class ProjectsViewTest(CommonTestCase):
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
        self._list(
            self.facililator,
            '/api/v1/projects/',
            status.HTTP_200_OK)

    def test_create(self):
        for data in [
            (self.beneficiary, status.HTTP_403_FORBIDDEN),
            (self.facililator, status.HTTP_201_CREATED),
                (self.investor, status.HTTP_403_FORBIDDEN)]:

            self._create(
                data[0],
                '/api/v1/projects/',
                {
                    'start': "2020-03-01",
                    'end': "2021-03-01",
                    'title': "My project",
                    'description': "Test",
                    'tasks': []
                }, data[1])

        self._create(
            self.facililator,
            '/api/v1/projects/',
            {
                'start': "2020-03-01",
                'end': "2020-03-01",
                'title': "My project",
                'description': "Test",
                'tasks': [{
                    'action': "Task!",
                    'reward': 0.0001
                }]
            }, status.HTTP_201_CREATED)

    def test_retrieve(self):
        self._retrieve(self.facililator,
                       f'/api/v1/projects/{self.project.id}/', status.HTTP_200_OK)

    def test_update(self):
        for data in [
            (self.beneficiary, status.HTTP_403_FORBIDDEN),
            (self.facililator, status.HTTP_200_OK),
                (self.investor, status.HTTP_403_FORBIDDEN)]:

            self._update(
                data[0],
                f'/api/v1/projects/{self.project.id}/',
                {
                    'start': "2020-03-01",
                    'end': "2020-03-01",
                    'title': "My project",
                    'description': "Test",
                    'tasks': [{
                        'action': "Task1",
                        'reward': 0.0001
                    },
                        {
                        'action': "Task2",
                        'reward': 0.0002
                    }]
                }, data[1])


class AssignmentViewTest(CommonTestCase):
    def setUp(self):
        self.beneficiary = CustomUser.objects.create(
            email="beneficiary@test.com",
            first_name="beneficiary",
            last_name="beneficiaryt",
            type=CustomUser.BENEFICIARY)

        self.beneficiary2 = CustomUser.objects.create(
            email="beneficiary@test2.com",
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

        self.assignment = Assignment.objects.create(
            beneficiary=self.beneficiary,
            project=self.project,
            status=Assignment.WAITING)

    def test_list(self):
        self._list(
            self.facililator,
            f"/api/v1/projects/{self.project.id}/assignments/",
            status.HTTP_200_OK)

        self._list(
            self.beneficiary,
            f"/api/v1/projects/{self.project.id}/assignments/",
            status.HTTP_403_FORBIDDEN)

        self._list(
            self.investor,
            f"/api/v1/projects/{self.project.id}/assignments/",
            status.HTTP_403_FORBIDDEN)

    def test_create(self):
        self._create(
            self.beneficiary2,
            f"/api/v1/projects/{self.project.id}/assignments/",
            {},
            status.HTTP_201_CREATED)

        self._create(
            self.facililator,
            f"/api/v1/projects/{self.project.id}/assignments/",
            {},
            status.HTTP_403_FORBIDDEN)

        self._create(
            self.investor,
            f"/api/v1/projects/{self.project.id}/assignments/",
            {},
            status.HTTP_403_FORBIDDEN)

    def test_update(self):
        self._update(
            self.beneficiary,
            f"/api/v1/projects/assignments/{self.assignment.id}/",
            {
                "beneficiary": {
                    "id": self.beneficiary.id,
                },
                "status": Assignment.REJECTED
            }, status.HTTP_403_FORBIDDEN)

        self._update(
            self.investor,
            f"/api/v1/projects/assignments/{self.assignment.id}/",
            {
                "beneficiary": {
                    "id": self.beneficiary.id,
                },
                "status": Assignment.REJECTED
            }, status.HTTP_403_FORBIDDEN)

        self._update(
            self.facililator,
            f"/api/v1/projects/assignments/{self.assignment.id}/",
            {
                "beneficiary": {
                    "id": self.beneficiary.id,
                },
                "status": Assignment.REJECTED
            }, status.HTTP_200_OK)
