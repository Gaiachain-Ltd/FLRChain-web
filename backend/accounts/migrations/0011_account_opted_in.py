# Generated by Django 3.2.12 on 2022-03-22 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20220210_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='opted_in',
            field=models.BooleanField(default=False),
        ),
    ]
