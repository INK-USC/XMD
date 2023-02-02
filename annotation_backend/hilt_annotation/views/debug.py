from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.views import APIView, Response, status
from ..models import Project, Document, Word, WordAnnotationScore, LocalExplanationDictionary, GlobalExplanationDictionary
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
            print(dataset_json)

            # call fastapi
            print('FastAPI call')
            req_url = "http://localhost:9000/debug/training"
            req_json = {
                "project_id": str(project.id),
                "from_local": False, ### NEEDS FIXING
                "dataset": dataset_json,
                "pretrained_model_name_or_path": pretrained_model_name_or_path
                }
            print('req_json', req_json)
            res = requests.post(req_url, json=req_json)

            if res.status_code == 201:
                project.debugging_status = 'running'
                return Response({'success': 'model started running'}, status.HTTP_202_ACCEPTED)
            else:
                return Response(data=res.text, status=500)

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
                'label': document.ground_truth.id,
                'before_expl_reg': score_before,
                'local_after_expl_reg': local_score_after,
                'global_after_expl_reg': global_score_after
            }
            instances.append(instance)
        
        return instances

## Views for fastapi status update

def add_debug_annotation_scores_and_model():
    """
    Create new model and annotation score entries in DB after training debugged model in FastAPI
    """
    pass

class TrainingDebugModelUpdate(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Get update after FAST API is done generating attributions
        """
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        add_debug_annotation_scores_and_model(request.data, project) # parse FastAPI payload and save in DB
        project.debugging_status = 'finished'
        project.save()

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