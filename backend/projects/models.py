from django.db import models
from projects.managers import ProjectManager, ProjectQuerySet


class Project(models.Model):
    FUNDRAISING = 0
    ACTIVE = 1
    CLOSED = 2

    STATUSES = (
        (FUNDRAISING, "Fundraising"),
        (ACTIVE, "Active"),
        (CLOSED, "Closed")
    )

    owner = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    beneficiaries = models.ManyToManyField(
        'users.CustomUser', through='Assignment', related_name='beneficiary_list')
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=CLOSED)
    milestones = models.ManyToManyField('projects.Milestone', related_name='milestones')
    fundraising_duration = models.PositiveSmallIntegerField(default=30)
    
    total = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    milestones_rewards = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    milestones_batch = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    milestones_total = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    fac_adm_funds = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    raised_total = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)

    objects = ProjectManager.from_queryset(ProjectQuerySet)()


class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    tasks = models.ManyToManyField('projects.Task', related_name='tasks')

    tasks_total = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    tasks_rewards = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    tasks_batch = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)


class Task(models.Model):
    name = models.CharField(max_length=255)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    reward = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    batch = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    count = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    total = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)


class Assignment(models.Model):
    REJECTED = 0
    ACCEPTED = 1
    WAITING = 2

    STATUS = (
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted'),
        (WAITING, 'Waiting'),
    )

    beneficiary = models.ForeignKey(
        'users.CustomUser', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(default=2, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('beneficiary', 'project')
