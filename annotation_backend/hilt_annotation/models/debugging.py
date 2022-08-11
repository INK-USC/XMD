import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from .document import Word, Label
from .project import Project
from .annotation import Annotation


class ModificationType(models.IntegerChoices):
    ADD = 0, _("Add")
    REMOVE = 1, _("Remove")


class WordAnnotationScore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name='word_annotation_score')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='word_annotation_score')
    score = models.FloatField(default=0.0)


class GlobalExplanationDictionary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.CharField(max_length=256)
    modification_type = models.IntegerField(choices=ModificationType.choices)
    ground_truth_label = models.ForeignKey(on_delete=models.CASCADE, related_name='ground_truth_global_exp', to=Label)
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
    modification_type = models.IntegerField(choices=ModificationType.choices)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='dict_local_explanation')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='dict_local_explanation')
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name='dict_local_explanation')

    class Meta:
        unique_together = (
            ('project', 'word', 'annotation'),
        )
