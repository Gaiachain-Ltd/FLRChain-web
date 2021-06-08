from django.db import models
# Create your models here.


class CirclePayment(models.Model):
    FAILED = 'failed'
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PAID = 'paid'

    STATUS = (
        (FAILED, "Failed"),
        (PENDING, "Peding"),
        (CONFIRMED, "Confirmed"),
        (PAID, "Paid")
    )

    id = models.CharField(max_length=255, primary_key=True, editable=False)
    amount = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    fee = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING)
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.SET_NULL, null=True)
    claimed = models.BooleanField(default=False)


class CircleTransfer(models.Model):
    FAILED = 'failed'
    PENDING = 'pending'
    COMPLETE = 'complete'

    STATUS = (
        (FAILED, "Failed"),
        (PENDING, "Pending"),
        (COMPLETE, "Complete")
    )

    id = models.CharField(max_length=255, primary_key=True, editable=False)
    amount = models.DecimalField(
        max_digits=26, decimal_places=6, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING)
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.SET_NULL, null=True)
    transaction = models.OneToOneField(
        'transactions.Transaction', on_delete=models.SET_NULL, null=True)
