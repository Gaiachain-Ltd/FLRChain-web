from django.db import models


class ProjectManager(models.Manager):
    def with_beneficiary_assignment_status(self, beneficiary):
        return self.annotate(assignment_status=models.Case(
            models.When(beneficiaries=beneficiary, then=models.F(
                'beneficiaries__assignment__status'))
        )).order_by('id', 'assignment_status').distinct('id')
