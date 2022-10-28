from rest_framework import serializers
from ..models.modelzip import Model

class ModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'project', 'name', 'description', 'model', 'uploaded_at']