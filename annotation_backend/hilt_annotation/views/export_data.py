import json
from django.http import HttpResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView, Response

from ..models import Project, GlobalExplanationDictionary, Document, LocalExplanationDictionary, Annotation


def get_json_export_data(project: Project):
    data = dict()
    global_words_qs = GlobalExplanationDictionary.objects.filter(project=project)
    all_global_words = dict()
    for global_ann in global_words_qs:
        all_global_words[global_ann.word] = {
            "id": str(global_ann.pk),
            "word": global_ann.word,
        }
    data["dictionary"] = list(all_global_words.values())
    docs = []
    for document in Document.objects.filter(project=project):
        doc = dict()
        doc["id"] = str(document.pk)
        doc["text"] = document.text
        doc["words"] = list(map(lambda x: x.text, document.words.order_by('order')))
        doc["annotated"] = document.annotated
        doc["metadata"] = document.metadata
        doc["belongs_to"] = document.belongs_to

        # annotations
        all_ann = []
        for ann in Annotation.objects.filter(document=document):
            all_ann.append({
                "id": str(ann.pk),
                "label": ann.label.text,
                "scores": list(map(lambda x: x.score, ann.word_annotation_score.order_by("word__order")))
            })
        if len(all_ann) > 0:
            doc["annotations"] = all_ann

        # explanations
        exp = []
        # global
        for word in doc["words"]:
            if word in all_global_words:
                tmp = all_global_words.get(word).copy()
                tmp["type"] = "global"
                exp.append(tmp)
        # local
        for local_exp in LocalExplanationDictionary.objects.filter(project=project, word__document=document):
            exp.append({
                "id": str(local_exp.pk),
                "type": "local",
                "word": local_exp.word.text
            })
        if len(exp) > 0:
            doc["explanations"] = exp
        docs.append(doc)
    data['data'] = docs
    return data


class DownloadData(APIView):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        filename = "_".join(project.name.lower().split())
        try:
            data = get_json_export_data(project)
            response = HttpResponse(content_type='text/json')
            response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(filename)
            response.write(json.dumps(data, ensure_ascii=False, indent=1))
            return response
        except Exception as e:
            return Response(exception=e)
