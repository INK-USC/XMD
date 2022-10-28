from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404

import os

from ..models import Project, Model


class ModelZipUpload(APIView):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        print(request.POST)
        try:
            name = request.POST['model_name']
            model_file = request.FILES['model_zip']
            cur_model = Model(name=name, project=project, model=model_file)
            cur_model.save()
            return Response({"success": "your file has been received"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(f'exception {e}')
            return Response(exception=e)



