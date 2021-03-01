from django.db import models

class Transaction(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True)
    explorer_link = models.CharField(max_length=128)
