# Generated by Django 3.2 on 2021-06-08 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0017_auto_20210513_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='action',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Opt-In action'), (1, 'Fueling action'), (2, 'Transfer'), (3, 'Close account'), (4, 'Investment'), (5, 'Beneficiary reward'), (6, 'Facilitator fee'), (7, 'Return investment'), (8, 'Top up')]),
        ),
    ]
