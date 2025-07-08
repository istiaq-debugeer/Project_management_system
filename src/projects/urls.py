from django.urls import path
from . import views

urlpatterns = [
    path(
        "projects/", views.ProjectListCreateView.as_view(), name="project-list-create"
    ),
    path(
        "projects/<int:pk>/",
        views.ProjectRetrieveUpdateDestroyView.as_view(),
        name="project-detail",
    ),
    path(
        "project-members/",
        views.ProjectMemberListCreateView.as_view(),
        name="projectmember-list-create",
    ),
    path(
        "project-members/<int:pk>/",
        views.ProjectDeleteView.as_view(),
        name="projectmember-detail",
    ),
]
