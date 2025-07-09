from rest_framework import generics, permissions
from .models import Project, ProjectMember
from .serializers import ProjectSerializer, ProjectMemberSerializer
from core.permissions import IsOwnerOrProjectAdmin
from rest_framework.views import APIView
from rest_framework.response import Response


class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrProjectAdmin]


class ProjectView(APIView):
    def get(self, request):

        role = request.query_params.get("role")
        owner_id = request.query_params.get("owner_id")

        queryset = (
            Project.objects.prefetch_related(
                "members",
            )
            .select_related("owner")
            .all()
        )

        if owner_id:
            queryset.filter(owner__id=owner_id)

        if role:
            queryset.filter(projectmember__role=role)

        serializer = ProjectSerializer(queryset, many=True)

        return Response(serializer.data)


class ProjectMemberListCreateView(generics.ListCreateAPIView):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectDeleteView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrProjectAdmin]
