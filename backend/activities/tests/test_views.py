from common.tests import CommonTestCase
from activities.models import Activity
from projects.models import Project, Task, Assignment
from users.models import CustomUser
from rest_framework import status
from accounts.models import Account
from investments.models import Investment
from smart_contracts.models import SmartContract
from algorand import utils
from django.core.files.uploadedfile import SimpleUploadedFile


class ActivitiesViewTest(CommonTestCase):
    fixtures = ['main_account.json', ]

    def setUp(self):
        self.beneficiary = CustomUser.objects.create(
            email="beneficiary@test.com",
            first_name="beneficiary",
            last_name="beneficiaryt",
            type=CustomUser.BENEFICIARY)

        self.beneficiary_account = Account.generate(self.beneficiary)

        self.facililator = CustomUser.objects.create(
            email="facililator@test.com",
            first_name="facililator",
            last_name="facililator",
            type=CustomUser.FACILITATOR)

        self.facililator_account = Account.generate(self.facililator)

        self.investor = CustomUser.objects.create(
            email="investor@test.com",
            first_name="investor",
            last_name="investor",
            type=CustomUser.INVESTOR)

        self.investor_account = Account.generate(self.investor)

        self.project = Project.objects.create(
            owner=self.facililator,
            start="2020-03-01",
            end="2021-03-01",
            title="Ma project",
            description="Test")

        self.task = Task.objects.create(
            project=self.project,
            action="Test",
            reward="0.001")

        self.project.tasks.add(self.task)
        self.project.save()

        self.assignment = Assignment.objects.create(
            beneficiary=self.beneficiary,
            project=self.project,
            status=Assignment.ACCEPTED)

        self.activity = Activity.objects.create(
            user=self.beneficiary,
            task=self.task,
            project=self.project,)

    def test_list(self):
        self._list(
            self.beneficiary, 
            f"/api/v1/projects/{self.project.id}/activities/",
            status.HTTP_200_OK)
        self._list(
            self.investor, 
            f"/api/v1/projects/{self.project.id}/activities/",
            status.HTTP_200_OK)
        self._list(
            self.facililator, 
            f"/api/v1/projects/{self.project.id}/activities/",
            status.HTTP_200_OK)
        
    def test_create(self):
        self.investment = Investment.objects.create(
            investor=self.investor,
            project=self.project,
            start="2020-03-01",
            end="2020-03-01",
            amount="0.1")
        self.investment.refresh_from_db()

        txids, _ = SmartContract.generate(self.investment)
        for txid in txids:
            utils.wait_for_confirmation(txid)

        small_jpg = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        file = SimpleUploadedFile('small.jpg', small_jpg, content_type='image/jpeg')
        self._create(
            self.facililator,
            f"/api/v1/projects/{self.project.id}/tasks/{self.task.id}/activities/",
            {
                "photo": file,
            },
            status.HTTP_403_FORBIDDEN, 'multipart')

        file = SimpleUploadedFile('small.jpg', small_jpg, content_type='image/jpeg')
        self._create(
            self.investor,
            f"/api/v1/projects/{self.project.id}/tasks/{self.task.id}/activities/",
            {
                "photo": file,
            },
            status.HTTP_403_FORBIDDEN, 'multipart')

        file = SimpleUploadedFile('small.jpg', small_jpg, content_type='image/jpeg')
        self._create(
            self.beneficiary,
            f"/api/v1/projects/{self.project.id}/tasks/{self.task.id}/activities/",
            {
                "photo": file,
            },
            status.HTTP_201_CREATED, 'multipart')