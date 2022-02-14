# Generated by Django 3.2.6 on 2022-02-10 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0025_auto_20220208_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='app_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='state',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Created'), (1, 'Initialized'), (2, 'Postponed'), (3, 'Started'), (4, 'Finished'), (5, 'Deleted')], default=0),
        ),
    ]