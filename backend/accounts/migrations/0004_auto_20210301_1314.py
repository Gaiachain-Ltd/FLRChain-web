# Generated by Django 3.1.7 on 2021-03-01 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_auto_20210223_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Normal account'), (1, 'Master account')], default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
