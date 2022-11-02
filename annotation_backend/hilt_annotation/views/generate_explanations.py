from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import generics, permissions, filters
from rest_framework.views import APIView, Response, status


from ..serializers import DocumentSerializer, LabelSerializer, WordGroupedSerializer, DocumentWordSerializer
from ..models import Project, HiltModel

# blash def view
class GenerateExplanations(APIView):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        try:
            use_huggingface = request.POST['useHuggingface']
            if use_huggingface:
                huggingface_str = request.POST['str']
            else:
                model_id = request.POST['model_id']
                model_path = request.POST['model_path']
                # or 
                model_obj = get_object_or_404(HiltModel, pk=model_id)
                model_path_2 = model_obj.model

            # make fastapi call

            return Response({'success': 'model started running'}, status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(exception=e)
        
# predefined = "hugging face model name"
# custom = "model id" -> extract to media/extracted_models/<project_id>/
# extra captum options -> do magic
# payload for fast api { model: "hugging face model name" | "media/extracted_models/<project_id>/" }
# model -> project.selected_model