# Generated by Django 3.2.12 on 2022-03-30 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_task_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='instructions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
