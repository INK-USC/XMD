from rest_framework import serializers
from ..models.document import Document, Label, Word


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'project', 'text', 'annotated', 'ground_truth', 'metadata']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'project', 'text', 'color_set']


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'document', 'text', 'order']


class WordWithDocSerializer(WordSerializer):
    document = DocumentSerializer(read_only=True)


class WordGroupedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['text']
