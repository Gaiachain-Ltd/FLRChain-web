# Generated by Django 3.2.12 on 2022-03-21 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_alter_activity_photos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='photos',
            field=models.ManyToManyField(blank=True, null=True, to='activities.Photo'),
        ),
    ]
