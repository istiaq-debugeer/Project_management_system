from django.urls import include, path
from .views import (
    UserListCreateView,
    UserRetrieveUpdateDestroyView,
    UserLoginView,
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(
    r"", UserListCreateView, basename="user"
)  # this will handle /users/ and /users/{id}/

urlpatterns = [
    path("create", include(router.urls)),
    # path("users/", UserListCreateView, name="user-list-create"),
    path(
        "users/<int:pk>/", UserRetrieveUpdateDestroyView.as_view(), name="user-detail"
    ),
    path("login/", UserLoginView.as_view(), name="user-login"),
]
