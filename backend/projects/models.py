from django.db import models


class Project(models.Model):
    owner = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    description = models.TextField(blank=True, null=True)
    beneficiaries = models.ManyToManyField(
        'users.CustomUser', related_name='beneficiaries')
    pending_beneficiaries = models.ManyToManyField(
        'users.CustomUser', related_name='pending_beneficiaries')
    tasks = models.ManyToManyField('projects.Task', related_name='tasks')


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    reward = models.PositiveIntegerField(default=0)


class Investment(models.Model):
    owner = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    
# class Activity(models.Model):
#     pass