from rest_framework import serializers
from ..models import Word, Annotation, Document, WordAnnotationScore, TaskTypes, SentimentAnalysisAnnotation, \
    RelationExtractionAnnotation


class WordAnnotationScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordAnnotationScore
        fields = ['annotation', 'score']  # , 'id', 'word']


class SentimentAnalysisAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentAnalysisAnnotation
        fields = ['pk']  # , 'annotation']


class RelationExtractionAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationExtractionAnnotation
        fields = ['pk', 'sbj_start_offset', 'sbj_end_offset', 'obj_start_offset', 'obj_end_offset']  # , 'annotation']


class AnnotationSerializer(serializers.ModelSerializer):
    extended_annotation = serializers.SerializerMethodField()

    def extended_annotation_serializer(self, instance):
        if instance.task == TaskTypes.SA:
            return SentimentAnalysisAnnotationSerializer
        elif instance.task == TaskTypes.RE:
            return RelationExtractionAnnotationSerializer
        else:
            return ValueError("Incorrect value for TaskType")

    def get_extended_annotation(self, instance):
        request = self.context.get('request')
        if request:
            extension = instance.get_extended_annotation()
            serializer = self.extended_annotation_serializer(instance)
            return serializer(extension).data

    class Meta:
        model = Annotation
        fields = ['id', 'task', 'label', 'extended_annotation']  # , 'document']


class WordSerializer(serializers.ModelSerializer):
    word_annotation_score = WordAnnotationScoreSerializer(many=True, read_only=True)

    class Meta:
        model = Word
        fields = ['id', 'text', 'order', 'word_annotation_score']  # , 'document']


class DocumentWordSerializer(serializers.ModelSerializer):
    words = WordSerializer(many=True, read_only=True)
    annotations = AnnotationSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'project', 'text', 'annotated', 'metadata', 'words', 'annotations']
