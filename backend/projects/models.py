from django.db import models


class Project(models.Model):
    owner = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    description = models.TextField(blank=True, null=True)
    beneficiaries = models.ManyToManyField(
        'users.CustomUser', through='Assignment', related_name='beneficiary_list')
    tasks = models.ManyToManyField('projects.Task', related_name='tasks')


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    reward = models.PositiveIntegerField(default=0)


class Assignment(models.Model):
    REJECTED = 0
    ACCEPTED = 1
    WAITING = 2

    STATUS = (
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted'),
        (WAITING, 'Waiting')
    )

    beneficiary = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(default=2)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('beneficiary', 'project')