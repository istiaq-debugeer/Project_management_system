from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from core.permissions import IsOwnerOrProjectAdmin
from projects.models import ProjectMember, Project
from tasks.serializers import CommentSerializer, TaskSerializer
from tasks.models import Task, Comments
from django.db.models import Prefetch

from users.models import User


permission_classes = [permissions.IsAuthenticated, IsOwnerOrProjectAdmin]


class TaskView(APIView):

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrProjectAdmin]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        query_dict = {}

        if project_id := request.query_params.get("project_id"):
            query_dict.update({"project_id": project_id})

        if assign_to := request.query_params.get("assign_to"):
            query_dict.update({"assign_to_id": assign_to})

        if status := request.query_params.get("status"):
            query_dict.update({"status": status})

        if priority := request.query_params.get("priority"):
            query_dict.update({"priority": priority})

        queryset = (
            Task.objects.filter(**query_dict)
            .select_related("project")
            .prefetch_related(Prefetch("assign_to", queryset=User.objects.all()))
        )

        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def put(self, request, task_id):
        if not task_id:
            return Response(
                {"detail": "Task ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, task_id):

        if not task_id:
            return Response(
                {"detail": "Task ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )

        task.delete()
        return Response(
            {"detail": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, comment_id):

        try:
            if comment_id:
                comment = (
                    Comments.objects.filter(id=comment_id)
                    .select_related("author")
                    .first()
                )
                if not comment:
                    return Response(
                        {"detail": "Comment not found."},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                serializer = CommentSerializer(comment)
                return Response(serializer.data)
            else:
                query_dict = {}

                if task_id := self.request.query_params.get("task_id"):
                    query_dict.update({"tasks": task_id})
                if user_id := self.request.query_params.get("user_id"):
                    query_dict.update({"user_id": user_id})

                # if not task_id:
                #     return Response(
                #         {"detail": "task_id is required"}, status=status.HTTP_400_BAD_REQUEST
                #     )

                queryset = (
                    Comments.objects.filter(**query_dict)
                    .select_related("author")
                    .order_by("-created_at")
                    .all()
                )
                serializer = CommentSerializer(queryset, many=True)
                return Response(serializer.data)
        except Exception as e:
            print(str(e))

    def put(self, request, comment_id):
        comment = Comments.objects.filter(id=comment_id).first()
        if not comment:
            return Response(
                {"detail": "Not found or permission denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = Comments.objects.filter(id=comment_id).first()
        if not comment:
            return Response(
                {"detail": "Not found or permission denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        comment.delete()
        return Response(
            {"detail": "Comment deleted."}, status=status.HTTP_204_NO_CONTENT
        )
