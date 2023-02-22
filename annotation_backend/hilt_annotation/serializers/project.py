from rest_framework import serializers
from ..models.project import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'task', 'created_at', 'updated_at', 'explanations_model', 'explanations_status', 'debugging_status']
