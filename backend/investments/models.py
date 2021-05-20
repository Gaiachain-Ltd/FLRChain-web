import datetime
from django.db import models, transaction
from transactions.models import Transaction
from accounts.models import Account
from django.core.exceptions import ObjectDoesNotExist


class Investment(models.Model):
    FINISHED = 0
    INVESTED = 1

    STATUS = (
        (FINISHED, 'Finished'),
        (INVESTED, 'Invested'),
    )

    investor = models.ForeignKey(
        'users.CustomUser', on_delete=models.SET_NULL, null=True)
    project = models.OneToOneField('projects.Project', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(default=INVESTED, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    start = models.DateField()
    end = models.DateField()
    amount = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)

    def finish(self):
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

            tx2 = Transaction.transfer(
                smart_contract.account,
                self.investor.account,
                0,
                Transaction.ALGO,
                Transaction.RETURN_INVESTMENT,
                self.investor.account,
                self.project)

            self.status = Investment.FINISHED
            self.save()

            return [tx1.txid, tx2.txid]

    @property
    def confirmed(self):
        try:
            return Transaction.objects.filter(
                to_account=self.smartcontract.account,
                status=Transaction.CONFIRMED,
                action=Transaction.INVESTMENT).exists()
        except ObjectDoesNotExist:
            return False