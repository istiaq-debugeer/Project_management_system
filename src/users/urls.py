from django.urls import include, path
from .views import (
    UserRegisterView,
    UserRetrieveUpdateDestroyView,
    UserLoginView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = DefaultRouter()
router.register(
    r"", UserRegisterView, basename="user"
)  # this will handle /users/ and /users/{id}/

urlpatterns = [
    path("create", include(router.urls)),
    # path("users/", UserListCreateView, name="user-list-create"),
    path(
        "users/<int:pk>/", UserRetrieveUpdateDestroyView.as_view(), name="user-detail"
    ),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
