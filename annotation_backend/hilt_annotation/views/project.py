from rest_framework import generics, permissions

from ..serializers import ProjectSerializer
from ..models import Project
from .permissions import IsOwner


class ProjectList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
