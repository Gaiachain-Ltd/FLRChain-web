# Generated by Django 3.2.12 on 2022-03-02 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_auto_20220302_1116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='state',
            new_name='sync',
        ),
    ]