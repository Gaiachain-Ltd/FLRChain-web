# Generated by Django 3.2.6 on 2022-02-10 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0026_auto_20220210_1111'),
        ('accounts', '0009_auto_20210401_0819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='smart_contract',
        ),
        migrations.AddField(
            model_name='account',
            name='project',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.project'),
        ),
    ]