from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination

from ..serializers.debugging import DictionarySerializer
from ..models import Dictionary, Project


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class DictionaryList(generics.ListCreateAPIView):
    queryset = Dictionary.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DictionarySerializer
    pagination_class = LargeResultsSetPagination
    search_fields = ('word',)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_id'))
        serializer.save(project=project)


class DictionaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dictionary.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DictionarySerializer

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])