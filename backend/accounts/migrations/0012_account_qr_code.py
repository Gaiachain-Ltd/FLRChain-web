# Generated by Django 3.2.12 on 2022-03-28 13:22

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_account_opted_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.upload_qr_code),
        ),
    ]
