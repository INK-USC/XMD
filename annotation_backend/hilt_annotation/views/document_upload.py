import json
import ijson

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from ..models import Project, Document, Label, Word, BelongsToLabel, Annotation, SentimentAnalysisAnnotation, \
    RelationExtractionAnnotation, TaskTypes, WordAnnotationScore


class ImportFileError(Exception):
    def __init__(self, message):
        self.message = message


def extract_metadata_json(entry):
    if "metadata" in entry:
        return json.dumps(entry["metadata"])
    else:
        temp = {}
        ignore_keys = {"id", "project", "text", "annotated", "metadata", "annotations", "belongs_to", "words"}
        for key in entry:
            if key not in ignore_keys:
                temp[key] = entry[key]
        return json.dumps(temp)


def map_dataset_label(belongs_to: str) -> BelongsToLabel:
    belongs_to = belongs_to.lower()
    if belongs_to == "dev":
        return BelongsToLabel.DEV
    elif belongs_to == "test":
        return BelongsToLabel.TEST
    return BelongsToLabel.TRAIN


def create_annotations(annotations, all_annotation_labels, max_color_set, project, current_doc):
    for annotation in annotations:
        # create base annotation
        cur_annotation = Annotation(task=project.task,
                                    document=current_doc,
                                    label=all_annotation_labels[str(current_doc.ground_truth)])

        cur_annotation.save()

        # Task extended annotation
        if project.task == TaskTypes.SA:
            ex_annotation = SentimentAnalysisAnnotation(annotation=cur_annotation)
            ex_annotation.save()

        if project.task == TaskTypes.RE:
            ex_annotation = RelationExtractionAnnotation(annotation=cur_annotation,
                                                         sbj_start_offset=annotation["sbj_start_offset"],
                                                         sbj_end_offset=annotation["sbj_end_offset"],
                                                         obj_start_offset=annotation["obj_start_offset"],
                                                         obj_end_offset=annotation["obj_end_offset"])
            ex_annotation.save()

    return max_color_set


def create_docs_from_json(project, data_file):
    # load previous
    all_annotation_labels = {}
    max_color_set = -1
    for label in Label.objects.filter(project=project):
        all_annotation_labels[label.text] = label
        max_color_set = max(max_color_set, label.color_set)

    try:
        if data_file.multiple_chunks():
            data = ijson.items(data_file, "data.item")
        else:
            data = json.load(data_file)
            data = data["data"]
    except:
        raise ImportFileError("Document dictionaries do not have the 'data' key")

    with transaction.atomic():
        for entry in data:
            try:
                text = entry["text"]
                # words = entry["words"]
            except:
                raise ImportFileError("Document dictionaries do not have the 'text' or 'words' key")

            metadata = extract_metadata_json(entry)
            annotations = entry.get("annotations", [{}])
            belongs_to = map_dataset_label(entry.get("belongs_to", ""))
            cur_doc = Document(text=text, metadata=metadata, project=project, belongs_to=belongs_to)
            ground_truth = entry.get("label", None)
            if ground_truth is not None:
                if ground_truth not in all_annotation_labels:
                    max_color_set += 1
                    new_label = Label(text=ground_truth, project=project, color_set=max_color_set)
                    new_label.save()
                    all_annotation_labels[ground_truth] = new_label
                cur_doc.ground_truth = all_annotation_labels[ground_truth]
            cur_doc.save()

            max_color_set = create_annotations(
                annotations,
                all_annotation_labels,
                max_color_set,
                project,
                cur_doc
            )


class DocumentUpload(APIView):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        import_format = request.POST['format']
        try:
            data_file = request.FILES['dataset']
            if import_format == 'json':
                create_docs_from_json(project, data_file)
            else:
                raise ImportFileError("'%s' file type not supported" % import_format)
            return Response({"success": "your file has been received"}, status=status.HTTP_202_ACCEPTED, )
        except ImportFileError as e:
            return Response(exception=e)
        except Exception as e:
            return Response(exception=e)
