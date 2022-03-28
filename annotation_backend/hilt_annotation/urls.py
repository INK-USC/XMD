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
    # Labels
    path('projects/<int:project_id>/labels/', views.LabelList.as_view(), name="labels-list"),
    path('projects/<int:project_id>/labels/<str:pk>/', views.LabelDetail.as_view(), name="labels-rud"),
    # Words
]
