import os
import shutil
import zipfile
from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import generics, permissions, filters
from rest_framework.views import APIView, Response, status
import requests


from ..serializers import DocumentSerializer, LabelSerializer, WordGroupedSerializer, DocumentWordSerializer
from ..models import Project, HiltModel, Document


class GenerateExplanations(APIView):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        try:
            use_huggingface = request.POST['useHuggingface']
            if use_huggingface == 'true':
                huggingface_str = request.POST['str']
                pretrained_model_name_or_path = request.POST['str']
                print(f'huggingface_model: {huggingface_str}')
            else:
                model_id = request.POST['model_id']
                model_obj = get_object_or_404(HiltModel, pk=model_id)
                model_path = model_obj.model.name
                model_abs_path = os.path.join(settings.MEDIA_ROOT, model_path)

                # LOCAL MODEL PATH
                # make/navigate to path
                # filekeeping
                unzip_path = os.path.join(settings.MEDIA_ROOT, 'unziped_models', str(project.id), 'tmp')
                os.makedirs(unzip_path, exist_ok=True)
                if len(os.listdir(unzip_path))!=0:
                    for f in os.listdir(unzip_path):
                        shutil.rmtree(os.path.join(unzip_path, f))

                #   unzip
                with zipfile.ZipFile(model_abs_path, 'r') as zip_ref:
                    zip_ref.extractall(unzip_path)
                unzip_path_folder = os.path.join(unzip_path, os.listdir(unzip_path)[0])

                pretrained_model_name_or_path = unzip_path_folder
                print(f'model_id: {model_id} \nmodel__abs_path: {model_abs_path} \nmodel_unziped_folder_path{unzip_path_folder}')


            dataset_json = self.generate_dataset_for_captum_call(project)

            # MAKE FASTAPI CALL
            print('FastAPI call')
            req_url = "http://localhost:9000/training/captum"
            req_json = {
                "from_local": True if use_huggingface=='false' else False ,
                "dataset": dataset_json,
                "pretrained_model_name_or_path": pretrained_model_name_or_path
                }
            res = requests.post(req_url, json=req_json)

            if res.status_code == 201:
                # model -> project.selected_model
                return Response({'success': 'model started running'}, status.HTTP_202_ACCEPTED)
            else:
                return Response(data=res.text, status=500)

        except Exception as e:
            print(e)
            return Response(exception=e)



    def generate_dataset_for_captum_call(self, project: Project):
        text, labels = [], []
        for data in Document.objects.filter(project=project):
            text.append(data.text)
            labels.append(data.ground_truth.id)

        print(text, labels)

        return {
            'text': text,
            'labels': labels 
        }

# predefined = "hugging face model name"
# custom = "model id" -> extract to media/extracted_models/<project_id>/
# extra captum options -> do magic
# payload for fast api { model: "hugging face model name" | "media/extracted_models/<project_id>/" }
# model -> project.selected_model
