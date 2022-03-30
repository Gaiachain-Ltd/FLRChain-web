import projects.models
from django.db import models


class ProjectQuerySet(models.QuerySet):
    def with_sum_spent_transactions(self):
        from transactions.models import Transaction
        return self.annotate(
            spent=models.Subquery(
                Transaction.objects.filter(
                    models.Q(
                        action=Transaction.REWARD, 
                        status__in=[Transaction.CONFIRMED, Transaction.PENDING]) | models.Q(
                        action=Transaction.FACILITATOR_FEE),
                    project=models.OuterRef('pk')).values('amount').annotate(
                        total_spent=models.Sum('amount')).values('total_spent')[:1]))


class ProjectManager(models.Manager):
    def with_beneficiary_assignment_status(self, beneficiary):
        assignments = projects.models.Assignment.objects.filter(
            beneficiary=beneficiary,
            project=models.OuterRef('pk'))
        return self.annotate(
            assignment_status=models.Subquery(assignments.values('status')[:1]))

    def for_investor(self, investor):
        from investments.models import Investment
        investments = Investment.objects.filter(
            investor=investor,
            project=models.OuterRef('pk')
        )
        return self.annotate(
            invested=models.Exists(investments)
        )
