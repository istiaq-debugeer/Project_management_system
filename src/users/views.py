from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


# users/views.py
class UserListCreateView(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserRegisterSerializer
        return UserSerializer

    # def get_permissions(self):
    #     if self.request.method == "POST":
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.save()

        return Response(data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserLoginView(TokenObtainPairView):

    permission_classes = [permissions.AllowAny]
