# Generated by Django 3.1.7 on 2021-04-01 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_transaction_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='action',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Opt-In action'), (1, 'Fueling action'), (2, 'Transfer'), (3, 'Close account'), (4, 'Investment'), (5, 'Beneficiary reward'), (6, 'Facilitator fee'), (7, 'Return investment')]),
        ),
    ]
