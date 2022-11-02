from rest_framework import serializers
from ..models.modelzip import HiltModel

class ModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiltModel
        fields = ['id', 'project', 'name', 'description', 'model', 'uploaded_at']