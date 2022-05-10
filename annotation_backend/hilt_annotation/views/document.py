from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import generics, permissions, filters

from ..serializers import DocumentSerializer, LabelSerializer, WordGroupedSerializer, DocumentWordSerializer
from ..models import Document, Label, Word
from .util import LargeResultsSetPagination


class DocumentList(generics.ListAPIView):
    queryset = Document.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer
    search_fields = ('text',)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        annotated_count = queryset.filter(annotated=True).count()

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response({'annotatedCount': annotated_count, "results": serializer.data})

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])


class LabelList(generics.ListAPIView):
    queryset = Label.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LabelSerializer

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])


class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LabelSerializer

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])


class WordList(generics.ListAPIView):
    queryset = Word.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WordGroupedSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('text',)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return self.queryset.filter(document__project=self.kwargs['project_id']).values('text').annotate(
            score=Avg('word_annotation_score__score')).order_by('-score')


class WordDetails(generics.ListAPIView):
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentWordSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'], words__text=self.kwargs['word']).order_by(
            'pk')  # '-words__word_annotation_score__score')
