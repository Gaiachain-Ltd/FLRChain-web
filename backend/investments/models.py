from django.db import models


class Investment(models.Model):
    INITIAL = 0
    TO_SYNC = 1
    SYNCED = 2
    FAILED = 3

    STATES = (
        (INITIAL, "Initial"),
        (TO_SYNC, "To sync"),
        (SYNCED, "Synced"),
        (FAILED, "Failed")
    )

    investor = models.ForeignKey(
        'users.CustomUser', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    sync = models.PositiveSmallIntegerField(default=TO_SYNC, choices=STATES)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('investor', 'project')