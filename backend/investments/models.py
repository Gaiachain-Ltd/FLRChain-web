import datetime
from django.db import models, transaction
from transactions.models import Transaction
from accounts.models import Account


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

    def finish(self):
        # if (self.end + datetime.timedelta(days=1)) > datetime.datetime.now().date():
        #     return

        with transaction.atomic():
            smart_contract = self.smartcontract

            usdc_balance = smart_contract.account.usdc_balance()
            tx1 = Transaction.transfer(
                smart_contract.account,
                self.investor.account,
                0,
                Transaction.USDC,
                Transaction.RETURN_INVESTMENT,
                self.investor.account,
                self.project)

            tx1.amount = usdc_balance
            tx1.save()

            Transaction.transfer(
                smart_contract.account,
                self.investor.account,
                0,
                Transaction.ALGO,
                Transaction.RETURN_INVESTMENT,
                self.investor.account,
                self.project)

            self.status = Investment.FINISHED
            self.save()