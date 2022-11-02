from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskTypes(models.IntegerChoices):
    SA = 1, _("Sequence Classification")
    RE = 2, _("Relation Extraction")


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    task = models.IntegerField(default=TaskTypes.SA, choices=TaskTypes.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_projects')
    selected_model = models.CharField(max_length=512, default=None, null=True)
