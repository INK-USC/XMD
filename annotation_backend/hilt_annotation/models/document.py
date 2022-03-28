import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from .project import Project


class BelongsToLabel(models.IntegerChoices):
    TRAIN = 0, _("Train")
    DEV = 1, _("Dev")
    TEST = 2, _("Test")


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    text = models.TextField()
    annotated = models.BooleanField(default=False)
    metadata = models.TextField(default='{}')
    belongs_to = models.IntegerField(default=BelongsToLabel.TRAIN, choices=BelongsToLabel.choices)

    class Meta:
        indexes = [
            models.Index(fields=["project"], name="document_project_index")
        ]


class Label(models.Model):
    text = models.CharField(max_length=30)
    project = models.ForeignKey(Project, related_name='labels', on_delete=models.CASCADE)
    color_set = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = (
            ('project', 'text'),
            ('project', 'color_set')
        )


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="words")
    text = models.CharField(max_length=256)
    order = models.PositiveIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["document"], name="word_document_index")
        ]
        ordering = ('order',)
