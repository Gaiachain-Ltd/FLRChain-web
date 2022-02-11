from django.db import models
from projects.managers import ProjectManager, ProjectQuerySet


def upload_project_image(instance, filename):
    return f"projects/{instance.pk}/images/{filename}"

def upload_project_document(instance, filename):
    return f"projects/{instance.pk}/documents/{filename}"

class Project(models.Model):
    FUNDRAISING = 0
    ACTIVE = 1
    CLOSED = 2

    STATUSES = (
        (FUNDRAISING, "Fundraising"),
        (ACTIVE, "Active"),
        (CLOSED, "Closed")
    )

    INITIAL = 0
    CREATED = 1
    INITIALIZED = 2
    POSTPONED = 3
    STARTED = 4
    FINISHED = 5
    DELETED = 6

    STATES = (
        (INITIAL, "Initial"),
        (CREATED, "Created"),
        (INITIALIZED, "Initialized"),
        (POSTPONED, "Postponed"),
        (STARTED, "Started"),
        (FINISHED, "Finished"),
        (DELETED, "Deleted")
    )

    owner = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)

    image = models.FileField(upload_to=upload_project_image, null=True, blank=True)
    document = models.FileField(upload_to=upload_project_document, null=True, blank=True)
    budget = models.FileField(upload_to=upload_project_document, null=True, blank=True)

    status = models.PositiveSmallIntegerField(choices=STATUSES, default=FUNDRAISING)
    state = models.PositiveSmallIntegerField(choices=STATES, default=INITIAL)

    start = models.DateField()
    end = models.DateField()

    beneficiaries = models.ManyToManyField(
        'users.CustomUser', 
        through='Assignment', 
        related_name='beneficiary_list'
    )
        
    milestones = models.ManyToManyField('projects.Milestone', related_name='milestones')
    
    fac_adm_funds = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)

    app_id = models.IntegerField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = ProjectManager.from_queryset(ProjectQuerySet)()


class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    tasks = models.ManyToManyField('projects.Task', related_name='tasks')


class Task(models.Model):
    name = models.CharField(max_length=255)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    reward = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    batch = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    count = models.PositiveIntegerField(default=0)


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
