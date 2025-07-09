from django.urls import path
from .views import CommentView, TaskView

urlpatterns = [
    path("", TaskView.as_view(), name="task-list-create"),
    path("<int:task_id>/", TaskView.as_view(), name="task-detail"),
    path("comments/", CommentView.as_view(), name="comment-list-create"),
    path("comments/<int:comment_id>/", CommentView.as_view(), name="comment-detail"),
]
