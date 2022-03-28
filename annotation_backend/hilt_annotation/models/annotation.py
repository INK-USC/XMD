import uuid
from django.core.exceptions import ValidationError
from django.db import models

from .document import Document, Label
from .project import TaskTypes


class Annotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prob = models.FloatField(default=0.0)
    task = models.IntegerField(default=TaskTypes.SA, choices=TaskTypes.choices)
    document = models.ForeignKey(on_delete=models.CASCADE, related_name='annotations', to=Document)
    label = models.ForeignKey(on_delete=models.CASCADE, related_name='annotations', to=Label)

    def get_extended_annotation(self):
        if self.task == TaskTypes.SA:
            return self.sentiment_analysis_annotation
        elif self.task == TaskTypes.RE:
            return self.relation_extraction_annotation
        else:
            return ValueError("Incorrect value for TaskType")


class SentimentAnalysisAnnotation(models.Model):
    annotation = models.OneToOneField(to=Annotation, on_delete=models.CASCADE,
                                      related_name='sentiment_analysis_annotation', primary_key=True)


class RelationExtractionAnnotation(models.Model):
    annotation = models.OneToOneField(to=Annotation, on_delete=models.CASCADE,
                                      related_name='relation_extraction_annotation')
    sbj_start_offset = models.PositiveIntegerField()
    sbj_end_offset = models.PositiveIntegerField()
    obj_start_offset = models.PositiveIntegerField()
    obj_end_offset = models.PositiveIntegerField()

    def clean(self):
        if self.sbj_start_offset >= self.sbj_end_offset:
            raise ValidationError("sbj_start_offset is after sbj_end_offset")

        if self.obj_start_offset >= self.obj_end_offset:
            raise ValidationError("obj_start_offset is after obj_end_offset")

        if self.sbj_end_offset >= self.obj_start_offset >= self.sbj_start_offset:
            raise ValidationError("Object starts in the middle of the Subject")

        if self.obj_end_offset >= self.sbj_start_offset >= self.obj_start_offset:
            raise ValidationError("Subject starts in the middle of the Object")
