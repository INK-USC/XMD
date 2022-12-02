from django.db import models
from .project import Project
import uuid

class HiltModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="models")
    description = models.CharField(max_length=255, blank=True)
    model = models.FileField(upload_to='models/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.model.delete()
        super.delete(*args, **kwargs)