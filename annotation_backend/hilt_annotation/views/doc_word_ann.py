from rest_framework import generics, permissions

from ..serializers.doc_word_ann import DocumentWordSerializer
from ..models.document import Document


class DocWordAnnDetail(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentWordSerializer

    def get_queryset(self):
        return self.queryset.filter(project=self.kwargs['project_id'])
