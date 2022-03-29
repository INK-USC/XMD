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
    path('projects/<int:project_id>/docs/<str:pk>/', views.DocumentDetail.as_view(), name="docs-rd"),
    # 1-Document - words, annotations, scores
    path('projects/<int:project_id>/docs/<str:pk>/words-annotations/', views.DocWordAnnDetail.as_view(),
         name="doc-words-ann-r"),
    # Labels
    path('projects/<int:project_id>/labels/', views.LabelList.as_view(), name="labels-list"),
    path('projects/<int:project_id>/labels/<str:pk>/', views.LabelDetail.as_view(), name="labels-rud"),
    # dictionary
    path('projects/<int:project_id>/dict/', views.DictionaryList.as_view(), name="dict-list-c"),
    path('projects/<int:project_id>/dict/<int:pk>/', views.DictionaryDetail.as_view(), name="dict-rud"),
]
