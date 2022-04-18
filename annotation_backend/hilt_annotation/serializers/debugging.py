from rest_framework import serializers

from ..models.debugging import GlobalExplanationDictionary, LocalExplanationDictionary
from .document import WordSerializer


class GlobalExplanationDictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalExplanationDictionary
        fields = ['id', 'word']


class LocalExplanationDictionaryListSerializer(serializers.ModelSerializer):
    word = WordSerializer()

    class Meta:
        model = LocalExplanationDictionary
        fields = ['id', 'word', 'annotation']


class LocalExplanationDictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalExplanationDictionary
        fields = ['id', 'word', 'annotation']
