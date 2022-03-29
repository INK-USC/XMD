from rest_framework import serializers
from ..models.debugging import Dictionary


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['id', 'annotation', 'word', 'project', 'explanation_type']
