from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from zipfile import ZipFile

import os

from ..models import Project, HiltModel


class ModelZipUpload(APIView):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        print(request.POST)
        try:
            model_file = request.FILES['model_zip']
            name =  str(kwargs.get('project_id')) + '_' + model_file.name
            model_file.name  = name
            cur_model = HiltModel(name=name, project=project, model=model_file)
            cur_model.save()
            return Response({"success": "your file has been received"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(f'exception {e}')
            return Response(exception=e)



