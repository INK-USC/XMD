# Generated by Django 4.0.3 on 2023-02-19 22:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('prob', models.FloatField(default=0.0)),
                ('task', models.IntegerField(choices=[(1, 'Sequence Classification'), (2, 'Relation Extraction')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('annotated', models.BooleanField(default=False)),
                ('metadata', models.TextField(default='{}')),
                ('belongs_to', models.IntegerField(choices=[(0, 'Train'), (1, 'Dev'), (2, 'Test')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='HiltModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('model', models.FileField(upload_to='models/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('debug', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=256)),
                ('order', models.PositiveIntegerField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='hilt_annotation.document')),
            ],
        ),
        migrations.CreateModel(
            name='SentimentAnalysisAnnotation',
            fields=[
                ('annotation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='sentiment_analysis_annotation', serialize=False, to='hilt_annotation.annotation')),
            ],
        ),
        migrations.CreateModel(
            name='WordDebugAnnotationScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('score', models.FloatField(default=0.0)),
                ('annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_debug_annotation_score', to='hilt_annotation.annotation')),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='word_debug_annotation_score', to='hilt_annotation.hiltmodel')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_debug_annotation_score', to='hilt_annotation.word')),
            ],
        ),
        migrations.CreateModel(
            name='WordAnnotationScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('score', models.FloatField(default=0.0)),
                ('annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_annotation_score', to='hilt_annotation.annotation')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_annotation_score', to='hilt_annotation.word')),
            ],
        ),
        migrations.CreateModel(
            name='RelationExtractionAnnotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sbj_start_offset', models.PositiveIntegerField()),
                ('sbj_end_offset', models.PositiveIntegerField()),
                ('obj_start_offset', models.PositiveIntegerField()),
                ('obj_end_offset', models.PositiveIntegerField()),
                ('annotation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='relation_extraction_annotation', to='hilt_annotation.annotation')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('task', models.IntegerField(choices=[(1, 'Sequence Classification'), (2, 'Relation Extraction')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('explanations_model', models.CharField(default=None, max_length=512, null=True)),
                ('explanations_status', models.CharField(default=None, max_length=512, null=True)),
                ('debugging_status', models.CharField(default=None, max_length=512, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LocalExplanationDictionary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('modification_type', models.IntegerField(choices=[(0, 'Add'), (1, 'Remove')])),
                ('annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dict_local_explanation', to='hilt_annotation.annotation')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dict_local_explanation', to='hilt_annotation.project')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dict_local_explanation', to='hilt_annotation.word')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=30)),
                ('color_set', models.PositiveSmallIntegerField(default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='hilt_annotation.project')),
            ],
        ),
        migrations.AddField(
            model_name='hiltmodel',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='hilt_annotation.project'),
        ),
        migrations.CreateModel(
            name='GlobalExplanationDictionary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('word', models.CharField(max_length=256)),
                ('modification_type', models.IntegerField(choices=[(0, 'Add'), (1, 'Remove')])),
                ('ground_truth_label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ground_truth_global_exp', to='hilt_annotation.label')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dict_global_explanation', to='hilt_annotation.project')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='ground_truth',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ground_truth_document', to='hilt_annotation.label'),
        ),
        migrations.AddField(
            model_name='document',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='hilt_annotation.project'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to='hilt_annotation.document'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to='hilt_annotation.label'),
        ),
        migrations.AddIndex(
            model_name='word',
            index=models.Index(fields=['document'], name='word_document_index'),
        ),
        migrations.AddIndex(
            model_name='word',
            index=models.Index(fields=['text'], name='word_text_index'),
        ),
        migrations.AlterUniqueTogether(
            name='localexplanationdictionary',
            unique_together={('project', 'word', 'annotation')},
        ),
        migrations.AlterUniqueTogether(
            name='label',
            unique_together={('project', 'text')},
        ),
        migrations.AddIndex(
            model_name='globalexplanationdictionary',
            index=models.Index(fields=['project'], name='dictionary_project_index'),
        ),
        migrations.AlterUniqueTogether(
            name='globalexplanationdictionary',
            unique_together={('project', 'word')},
        ),
        migrations.AddIndex(
            model_name='document',
            index=models.Index(fields=['project'], name='document_project_index'),
        ),
    ]
