from django.db import models


class Activity(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    task = models.ForeignKey('projects.Task', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    photo = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)