from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from ..serializers.debugging import GlobalExplanationDictionarySerializer, LocalExplanationDictionarySerializer, \
    LocalExplanationDictionaryListSerializer
from ..models import GlobalExplanationDictionary, Project, LocalExplanationDictionary
from .util import LargeResultsSetPagination


class GlobalExplanationDictionaryList(generics.ListCreateAPIView):
    queryset = GlobalExplanationDictionary.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GlobalExplanationDictionarySerializer
    pagination_class = LargeResultsSetPagination
    search_fields = ('word',)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_id'))
        serializer.save(project=project)


class GlobalExplanationDictionaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GlobalExplanationDictionary.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GlobalExplanationDictionarySerializer

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])


class LocalExplanationDictionaryList(generics.ListCreateAPIView):
    queryset = LocalExplanationDictionary.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        q = self.queryset.filter(project=self.kwargs['project_id'])
        if 'doc_id' in self.request.query_params:
            q = q.filter(annotation__document=self.request.query_params['doc_id'])
        return q

    def get_serializer_class(self):
        if self.request.method == "GET":
            return LocalExplanationDictionaryListSerializer
        return LocalExplanationDictionarySerializer

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_id'))
        serializer.save(project=project)


class LocalExplanationDictionaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocalExplanationDictionary.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LocalExplanationDictionarySerializer

    # def get_queryset(self):
    #     return self.queryset.filter(annotation__document=self.kwargs['doc_id'])
