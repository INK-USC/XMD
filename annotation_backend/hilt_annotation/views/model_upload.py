import uuid
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper

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


class ModelDownload(APIView):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        try:
            model_id = uuid.UUID(request.POST['model_id'])
            model = HiltModel.objects.filter(project=project, id=model_id)[0]
            path = str(model.model)
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            print('total file path:', file_path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/zip")
                    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                    return response
        except Exception as e:
            print(f'exception {e}')
            return Response(exception=e)

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     return Response({"success": "your file has been received"}, status=status.HTTP_202_ACCEPTED)


