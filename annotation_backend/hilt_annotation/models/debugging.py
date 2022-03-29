import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from .document import Word
from .project import Project
from .annotation import Annotation


class ExplanationTypes(models.IntegerChoices):
    LOCAL = 1, _("Local Explanation")
    GLOBAL = 2, _("Global Explanation")


class WordAnnotationScore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name='word_annotation_score')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='word_annotation_score')
    score = models.FloatField(default=0.0)


class Dictionary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    annotation = models.ForeignKey(Annotation, null=True, on_delete=models.SET_NULL, related_name='project_dictionary')
    word = models.CharField(max_length=256)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_dictionary')
    explanation_type = models.IntegerField(default=ExplanationTypes.LOCAL, choices=ExplanationTypes.choices)

    class Meta:
        unique_together = (
            ('project', 'word'),
        )
        indexes = [
            models.Index(fields=["project"], name="dictionary_project_index")
        ]
