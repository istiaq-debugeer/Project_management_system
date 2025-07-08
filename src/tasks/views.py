from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from projects.models import ProjectMember, Project
from .serializers import TaskSerializer
from tasks.models import Task


class CreateTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        project_id = request.data.get("project")
        user = request.user

        is_admin = ProjectMember.objects.filter(
            project_id=project_id, user=user, role="admin"
        ).exists()

        if not is_admin:
            return Response(
                {"detail": "Only project admins can create tasks."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # If the user is admin, proceed to create task
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
