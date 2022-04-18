import uuid
from django.db import models

from .document import Word
from .project import Project
from .annotation import Annotation


class WordAnnotationScore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name='word_annotation_score')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='word_annotation_score')
    score = models.FloatField(default=0.0)


class GlobalExplanationDictionary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.CharField(max_length=256)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='dict_global_explanation')

    class Meta:
        unique_together = (
            ('project', 'word'),
        )
        indexes = [
            models.Index(fields=["project"], name="dictionary_project_index")
        ]


class LocalExplanationDictionary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='dict_local_explanation')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='dict_local_explanation')
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name='dict_local_explanation')

    class Meta:
        unique_together = (
            ('project', 'word', 'annotation'),
        )
