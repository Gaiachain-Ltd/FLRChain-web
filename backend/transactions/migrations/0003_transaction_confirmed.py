# Generated by Django 3.1.7 on 2021-03-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20210322_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
