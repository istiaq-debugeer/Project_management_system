from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.ProjectListCreateView.as_view(), name="project-list-create"),
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
    path("projects", views.ProjectView.as_view(), name="get_all_project"),
    path(
        "project-members/<int:pk>/",
        views.ProjectDeleteView.as_view(),
        name="projectmember-detail",
    ),
]
