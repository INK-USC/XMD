import os
import shutil
import uuid
import zipfile
from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import generics, permissions, filters
from rest_framework.views import APIView, Response, status
import requests


from ..serializers import DocumentSerializer, LabelSerializer, WordGroupedSerializer, DocumentWordSerializer, WordAnnotationScoreSerializer
from ..models import Project, HiltModel, Document, WordAnnotationScore, Word, Annotation


class ImportFileError(Exception):
    def __init__(self, message):
        self.message = message


class GenerateExplanations(APIView):
    def post(self, request, *args, **kwargs):
        """
        Generate Explanations from FAST API endpoint and update DBModel state.
        """
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

                # filekeeping
                unzip_path = os.path.join(settings.MEDIA_ROOT, 'unziped_models', str(project.id), 'tmp')
                os.makedirs(unzip_path, exist_ok=True)
                if len(os.listdir(unzip_path))!=0:
                    for f in os.listdir(unzip_path):
                        shutil.rmtree(os.path.join(unzip_path, f))

                #   unzip
                with zipfile.ZipFile(model_abs_path, 'r') as zip_ref: #causing delay
                    zip_ref.extractall(unzip_path)
                unzip_path_folder = os.path.join(unzip_path, os.listdir(unzip_path)[0])

                pretrained_model_name_or_path = unzip_path_folder
                print(f'model_id: {model_id} \nmodel__abs_path: {model_abs_path} \nmodel_unziped_folder_path{unzip_path_folder}')


            dataset_json = self._generate_dataset_for_captum_call(project)

            # MAKE FASTAPI CALL
            print('FastAPI call')
            req_url = "http://localhost:9000/generate/expl"
            req_json = {
                "project_id": str(project.id),
                "from_local": True if use_huggingface=='false' else False ,
                "dataset": dataset_json,
                "pretrained_model_name_or_path": pretrained_model_name_or_path
                }
            res = requests.post(req_url, json=req_json)

            if res.status_code == 201:
                project.explanations_status = 'running'
                project.explanations_model = pretrained_model_name_or_path
                project.save()
                print('project model changed status to running')
                return Response({'success': 'model started running'}, status.HTTP_202_ACCEPTED)
            else:
                return Response(data=res.text, status=500)

        except Exception as e:
            print(e)
            return Response(exception=e)

    def _generate_dataset_for_captum_call(self, project: Project):
        text, labels, document_ids = [], [], []
        for data in Document.objects.filter(project=project):
            text.append(data.text)
            labels.append(data.ground_truth.text)
            document_ids.append(str(data.id))

        print(text, labels)

        return {
            'text': text,
            'labels': labels,
            'metadata': {
                'document_ids': document_ids
            } 
        }


class GenerateSingleExplanations(APIView):
    def post(self, request, *args, **kwargs):
        try:
            print('request.POST', request.POST)
            project = get_object_or_404(Project, pk=kwargs.get('project_id'))
            model_id = request.POST['model_id']
            print('model_id', model_id)
            model_obj = get_object_or_404(HiltModel, pk=model_id)
            if not model_obj: raise ImportFileError("model_id is not valid")
            
            model_path = model_obj.model.name
            model_abs_path = os.path.join(settings.MEDIA_ROOT, model_path)
             # filekeeping
            unzip_path = os.path.join(settings.MEDIA_ROOT, 'unziped_models', str(project.id), 'debug_tmp')
            os.makedirs(unzip_path, exist_ok=True)
            if len(os.listdir(unzip_path))!=0:
                for f in os.listdir(unzip_path):
                    shutil.rmtree(os.path.join(unzip_path, f))

            #   unzip
            print('model_path', model_path)
            print('model_abs_path', model_abs_path)
            print('unzip_path', unzip_path)
            with zipfile.ZipFile(model_abs_path, 'r') as zip_ref: #causing delay
                zip_ref.extractall(unzip_path)
            unzip_path_folder = os.path.join(unzip_path, os.listdir(unzip_path)[0])

            full_path = unzip_path_folder
            print(f'model_id: {model_id} \nmodel__abs_path: {model_abs_path} \nmodel_unziped_folder_path{unzip_path_folder}')
            dataset = request.POST['text']

            # MAKE FASTAPI CALL
            print('FastAPI call')
            req_url = "http://localhost:9000/generate/expl/single"
            req_json = {
                "dataset": dataset,
                "model_path": full_path
                }
            print('req_json:', req_json)
            res = requests.post(req_url, json=req_json)

            if res.status_code == 201:
                return Response({'res': res.content}, status.HTTP_202_ACCEPTED) # check and return correct data
            else:
                return Response(data=res.text, status=500)

            # print('Inside GenerateSingleExplanations', request.POST)
            # return Response({'success': 'model started running'}, status.HTTP_202_ACCEPTED)


        except Exception as e:
            print(e)
            return Response(exception=e)


def add_annotation_scores(data, project: Project):
    '''Tables updated:
        1. WordAnnotationScore -> score
        2. Document -> annotated=True
        3. Project -> model_selected='finished'
    '''
    # 1
    for sentence in data:
        document_id = uuid.UUID(sentence['document_id'])
        document = Document.objects.filter(id=document_id)[0]
        # delete words and wordannotationscores
        delete_words_and_annotations(document)
        for idx, (word_str, score) in enumerate(zip(sentence['tokens'], sentence['before_reg_explanation'])):
            cur_word = Word(document=document, text=word_str, order=idx)
            cur_word.save()
            word = Word.objects.filter(document=document, order=idx)[0]
            wordannotationscore = WordAnnotationScore.objects.filter(word=word.id).first()
            if not wordannotationscore: # create row if word dosent exist in WordAnnotationScore table
                print('creating new obj')
                wordannotationscore = WordAnnotationScore(score=score, annotation=Annotation.objects.filter(document=document)[0], word=word)
            else: # else update score
                wordannotationscore.score = score
            print(wordannotationscore)
            wordannotationscore.save(())

        # 2
        document.annotated = True
        document.save()
        # 3
    project.explanations_status = 'finished'
    project.save()
    print('project model changed status to finished')


def delete_words_and_annotations(document: Document):
    words = Word.objects.filter(document=document)
    for word in words:
        wordannotationscore = WordAnnotationScore.objects.filter(word=word.id)
        wordannotationscore.delete()
    words.delete()
    print('deleted words and annotations')
    print('words:', Word.objects.filter(document=document))

class ExplAttrUpdate(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Get update after FAST API is done generating attributions
        """
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        add_annotation_scores(request.data, project)
        # for sentence in request.data:
        #     for word, score in zip(sentence['tokens'], sentence['before_reg_explanation']):
        #         print(f'{word}: {score}')
       
        return Response({"success": "attrs received"}, status=status.HTTP_202_ACCEPTED)

class ExplAttrGenerationStatus(APIView):
    def get(self, request, *args, **kwargs):
        """
        Endpoint hit by Vue to check explanation generation status
        """
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))  
        if project.explanations_status == 'running': # explanations still generating
            return Response({"status": "running"}, status=status.HTTP_200_OK)
        else: # explanations completed
            return Response({"status": "finished"}, status=status.HTTP_200_OK)


