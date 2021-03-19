import projects.models
from django.db import models


class ProjectManager(models.Manager):
    def with_beneficiary_assignment_status(self, beneficiary):
        assignments = projects.models.Assignment.objects.filter(
            beneficiary=beneficiary,
            project=models.OuterRef('pk'))
        return self.annotate(assignment_status=models.Subquery(assignments.values('status')[:1]))

    def for_investor(self, investor):
        return self.filter(
            models.Q(investment__isnull=True) | models.Q(investment__investor=investor))