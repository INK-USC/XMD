from django.urls import path
from . import views

# CRUD - create, retrieve, update, destroy
urlpatterns = [
    # project
    path('projects/', views.ProjectList.as_view(), name="project-list-c"),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name="project-rud"),
    # Documents
    path('projects/<int:project_id>/docs/', views.DocumentList.as_view(), name="docs-list"),
    path('projects/<int:project_id>/docs/upload/', views.DocumentUpload.as_view(), name="docs-upload"),
    path('projects/<int:project_id>/docs/<str:pk>/', views.DocumentDetail.as_view(), name="docs-rud"),
    # 1-Document - words, annotations, scores
    path('projects/<int:project_id>/docs/<str:pk>/words-annotations/', views.DocWordAnnDetail.as_view(),
         name="doc-words-ann-r"),
    # Labels
    path('projects/<int:project_id>/labels/', views.LabelList.as_view(), name="labels-list"),
    path('projects/<int:project_id>/labels/<str:pk>/', views.LabelDetail.as_view(), name="labels-rud"),
    # words
    path('projects/<int:project_id>/words/', views.WordList.as_view(), name="words-list"),
    path('projects/<int:project_id>/words/<str:word>/', views.WordDetails.as_view(), name="words-documents-list"),
    # dict global explanation
    path('projects/<int:project_id>/dict/global/', views.GlobalExplanationDictionaryList.as_view(), name="dict-list-c"),
    path('projects/<int:project_id>/dict/global/<str:pk>/', views.GlobalExplanationDictionaryDetail.as_view(),
         name="dict-rud"),
    # dict local explanation
    path('projects/<int:project_id>/dict/local/', views.LocalExplanationDictionaryList.as_view(),
         name="dict-local-list-c"),
    path('projects/<int:project_id>/dict/local/<str:pk>/', views.LocalExplanationDictionaryDetail.as_view(),
         name="dict-local-rud"),
    # Export data
    path('export/json/<int:project_id>/', views.DownloadData.as_view(), name="docs-export-json"),
    # Models
    path('projects/<int:project_id>/models/', views.ModelList.as_view(), name="models-list"),
    path('projects/<int:project_id>/models/upload/', views.ModelZipUpload.as_view(), name="models-upload"),
    path('projects/<int:project_id>/models/<str:pk>/', views.ModelDetail.as_view(), name="models-rud"),
    path('projects/<int:project_id>/explanations/', views.GenerateExplanations.as_view(), name="generate-explanations")
]
