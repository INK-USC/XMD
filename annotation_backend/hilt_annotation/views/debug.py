import io
import os
import shutil
import zipfile
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.files import File
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.views import APIView, Response, status
from ..models import Project, Document, Word, WordAnnotationScore, LocalExplanationDictionary, GlobalExplanationDictionary, HiltModel
import requests

class TrainingDebugModel(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        """
        Train model on debug data
        """
        print('TrainingDebugModel View')
        try:
            project = get_object_or_404(Project, pk=kwargs.get('project_id'))
            # extract debug data from request
            # get model from request

            # parse debug data into json format as needed by fastapi
            pretrained_model_name_or_path = project.explanations_model
            dataset_json = self._generate_json_for_debugging(project)
            # print(dataset_json)

            # call fastapi
            print('FastAPI call')
            req_url = "http://localhost:9000/debug/training"
            req_json = {
                "project_id": str(project.id),
                "from_local": False, ### NEEDS FIXING
                "dataset": dataset_json,
                "pretrained_model_name_or_path": pretrained_model_name_or_path
                }
            # print('req_json', req_json)
            res = requests.post(req_url, json=req_json)

            if res.status_code == 201:
                project.debugging_status = 'running'
                project.save()
                return Response({'success': 'model started running'}, status.HTTP_202_ACCEPTED)
            else:
                return Response(data=res.text, status=500)

            # ######## testing ########
            # _save_debug_model({'save_model_path': '/Users/kiran/XDrive/INK/HILT-demo/annotation_backend/media/debug_models/trial1'}, project)
            # return Response({'success': 'model started running'}, status.HTTP_202_ACCEPTED)

        except Exception as e:
            print(e)
            return Response(exception=e)
    
    def _generate_json_for_debugging(self, project):
        instances = []
        for document in Document.objects.filter(project=project):
            score_before = []
            local_score_after, global_score_after = [], []
            tokens = []
            for word in Word.objects.filter(document=document):
                tokens.append(word.text)
                word_annotation_score = WordAnnotationScore.objects.filter(word=word)[0]
                score_before.append(word_annotation_score.score)
                if LocalExplanationDictionary.objects.filter(word=word, project=project).exists():
                    local_explanation_word = LocalExplanationDictionary.objects.filter(word=word, project=project)[0]
                    local_score_after.append(float(local_explanation_word.modification_type))
                    print('local regularization')
                else:
                    local_score_after.append(word_annotation_score.score)
                if GlobalExplanationDictionary.objects.filter(word=word.text, project=project).exists():
                    global_explanation_word = GlobalExplanationDictionary.objects.filter(word=word.text, project=project)[0]
                    global_score_after.append(float(global_explanation_word.modification_type))
                    print('global regularization')
                else:
                    global_score_after.append(word_annotation_score.score)

            instance = {
                'document_id': str(document.id),
                'tokens': tokens,
                'label': document.ground_truth.text,
                'before_expl_reg': score_before,
                'local_after_expl_reg': local_score_after,
                'global_after_expl_reg': global_score_after
            }
            instances.append(instance)
        
        return instances

## Views for fastapi status update

def _save_debug_model(data, project):
    """
    Create new model and annotation score entries in DB after training debugged model in FastAPI
    """
    print(data)
    model_path = data['save_model_path'] # '/Users/kiran/XDrive/INK/HILT-demo/annotation_backend/media/debug_models/trial1'

    # create dir for zip location
    zip_save_path = os.path.join(settings.MEDIA_ROOT, 'unziped_models', str(project.id), 'tmp')
    print('zip_save_path', zip_save_path)
    os.makedirs(zip_save_path, exist_ok=True)
    if len(os.listdir(zip_save_path))!=0:
        for f in os.listdir(zip_save_path):
            f_abs_path = os.path.join(zip_save_path, f)
            if os.path.isfile(f_abs_path):
                os.remove(f_abs_path)
            else:
                shutil.rmtree(f_abs_path)
        

    name =  str(project.id) + '_' + 'debug_model'
    name_with_ext = name + '.zip'

    zip_full_path_without_ext = os.path.join(zip_save_path, name)
    print('zip_full_path', zip_full_path_without_ext)
    print('model_path', model_path)

    # buffer = io.BytesIO()

    # zip model
    shutil.make_archive(zip_full_path_without_ext, 'zip', model_path)
    print('zipped model')

    zip_full_path = zip_full_path_without_ext + '.zip'
    zip_destination_path = os.path.join(settings.MEDIA_ROOT, 'models', name_with_ext)
    # # save zip model in DB
    # move model in place 'media/models'
    os.replace(zip_full_path, zip_destination_path)

    # HiltModel save

    cur_model = HiltModel(name=name, project=project, debug=True)
    cur_model.model.name = os.path.join('models', name_with_ext)
    cur_model.save()
    print('model saved')



class TrainingDebugModelUpdate(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Get update after FAST API is done generating attributions
        """
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        _save_debug_model(request.data, project) # parse FastAPI payload and save in DB
        project.debugging_status = 'finished'
        project.save()

        return Response({"success": "model received"}, status=status.HTTP_202_ACCEPTED)
class TrainingDebugModelStatus(APIView):
    def get(self, request, *args, **kwargs):
        """
        Endpoint hit by Vue to check explanation generation status
        """
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        if project.debugging_status == 'running':
            return Response({"status": "running"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "finished"}, status=status.HTTP_200_OK)