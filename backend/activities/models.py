import uuid
from django.db import models


class Photo(models.Model):
    file = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Activity(models.Model):
    WAITING = 0
    ACCEPTED = 1
    REJECTED = 2

    STATUS = (
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted'),
        (WAITING, 'Waiting'),
    )

    INITIAL = 0
    TO_SYNC = 1
    SYNCED = 2

    STATES = (
        (INITIAL, "Initial"),
        (TO_SYNC, "To sync"),
        (SYNCED, "Synced")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey('projects.Task', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    reward = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    status = models.PositiveSmallIntegerField(default=WAITING, choices=STATUS)
    sync = models.PositiveSmallIntegerField(default=INITIAL, choices=STATES)

    photos = models.ManyToManyField(Photo)
    text = models.TextField(blank=True, null=True)
    area = models.IntegerField(null=True)
    number = models.IntegerField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
