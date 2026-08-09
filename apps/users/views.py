from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminUser
from .serializers import (
    UserCreateSerializer,
    UserSerializer,
)


User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    Administrative user management API.
    """

    queryset = User.objects.all().order_by("-created_at")

    permission_classes = (
        IsAdminUser,
    )

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer

        return UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        role = self.request.query_params.get(
            "role"
        )

        is_active = self.request.query_params.get(
            "is_active"
        )

        if role:
            queryset = queryset.filter(
                role=role
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower()
                in {"true", "1", "yes"}
            )

        return queryset