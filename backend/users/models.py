from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from users.managers import CustomUserManager
from transactions.models import Transaction


# source: https://tech.serhatteker.com/post/2020-01/email-as-username-django/
class CustomUser(AbstractUser):
    BENEFICIARY = 0
    FACILITATOR = 1
    INVESTOR = 2
    ADMINISTRATOR = 3

    USER_TYPES = (
        (BENEFICIARY, "Beneficiary"),
        (FACILITATOR, "Facilitator"),
        (INVESTOR, "Investor"),
        (ADMINISTRATOR, "Administrator"),
    )

    username = None
    email = models.EmailField(_('email address'), unique=True)
    type = models.PositiveSmallIntegerField(
        choices=USER_TYPES, default=BENEFICIARY)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=16, blank=True)
    village = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def opted_in(self):
        return Transaction.objects.filter(
            from_account__user=self,
            status=Transaction.CONFIRMED,
            action=Transaction.OPT_IN).exists()

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
