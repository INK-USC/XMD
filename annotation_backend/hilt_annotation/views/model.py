from rest_framework import generics, permissions
from ..models import Model
from ..serializers import ModelListSerializer

class ModelList(generics.ListAPIView):
    queryset = Model.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ModelListSerializer

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])

class ModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Model.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ModelListSerializer

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])