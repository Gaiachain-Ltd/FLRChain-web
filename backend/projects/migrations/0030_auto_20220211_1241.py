# Generated by Django 3.2.12 on 2022-02-11 12:41

from django.db import migrations, models
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0029_alter_project_app_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='budget',
            field=models.FileField(blank=True, null=True, upload_to=projects.models.upload_project_document),
        ),
        migrations.AlterField(
            model_name='project',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to=projects.models.upload_project_document),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=projects.models.upload_project_image),
        ),
    ]