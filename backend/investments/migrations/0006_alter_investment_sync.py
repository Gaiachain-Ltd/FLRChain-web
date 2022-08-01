# Generated by Django 3.2.12 on 2022-03-07 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0005_auto_20220307_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='sync',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Initial'), (1, 'To sync'), (2, 'Synced'), (3, 'Failed')], default=1),
        ),
    ]
