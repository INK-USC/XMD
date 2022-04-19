# Generated by Django 4.0.3 on 2022-04-18 07:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hilt_annotation', '0002_remove_dictionary_annotation_localexplanation'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalExplanationDictionary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('word', models.CharField(max_length=256)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dict_global_explanation', to='hilt_annotation.project')),
            ],
        ),
        migrations.CreateModel(
            name='LocalExplanationDictionary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dict_local_explanation', to='hilt_annotation.annotation')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dict_local_explanation', to='hilt_annotation.project')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dict_local_explanation', to='hilt_annotation.word')),
            ],
            options={
                'unique_together': {('project', 'word', 'annotation')},
            },
        ),
        migrations.RemoveField(
            model_name='localexplanation',
            name='annotation',
        ),
        migrations.RemoveField(
            model_name='localexplanation',
            name='dictionary',
        ),
        migrations.DeleteModel(
            name='Dictionary',
        ),
        migrations.DeleteModel(
            name='LocalExplanation',
        ),
        migrations.AddIndex(
            model_name='globalexplanationdictionary',
            index=models.Index(fields=['project'], name='dictionary_project_index'),
        ),
        migrations.AlterUniqueTogether(
            name='globalexplanationdictionary',
            unique_together={('project', 'word')},
        ),
    ]