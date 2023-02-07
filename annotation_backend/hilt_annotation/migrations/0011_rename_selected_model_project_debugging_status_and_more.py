# Generated by Django 4.0.3 on 2022-12-05 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hilt_annotation', '0010_rename_model_hiltmodel_project_selected_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='selected_model',
            new_name='debugging_status',
        ),
        migrations.AddField(
            model_name='project',
            name='explanations_model',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='explanations_status',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
    ]