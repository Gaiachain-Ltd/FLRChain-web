from django.db import models


class Investment(models.Model):
    FINISHED = 0
    INVESTED = 1

    STATUS = (
        (FINISHED, 'Finished'),
        (INVESTED, 'Invested'),
    )

    investor = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)
    project = models.OneToOneField('projects.Project', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(default=1, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    start = models.DateField()
    end = models.DateField()
    amount = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
