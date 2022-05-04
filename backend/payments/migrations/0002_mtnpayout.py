# Generated by Django 3.2.6 on 2021-12-16 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MTNPayout',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=6, default=0, max_digits=26)),
                ('fee', models.DecimalField(decimal_places=6, default=0, max_digits=26)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'Transfered (USDC)'), (2, 'Confirmed (USDC)'), (3, 'Requested (MTN)'), (4, 'Completed (MTN)')], default=0)),
                ('success', models.NullBooleanField(default=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
