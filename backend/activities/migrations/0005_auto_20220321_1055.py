# Generated by Django 3.2.12 on 2022-03-21 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_auto_20220321_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='area',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
