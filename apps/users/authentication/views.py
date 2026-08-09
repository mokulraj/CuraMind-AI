from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from rest_framework_simplejwt.exceptions import (
    TokenError,
)

from rest_framework_simplejwt.tokens import (
    RefreshToken,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from apps.users.authentication.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    UserMeSerializer,
)

from apps.users.authentication.services import (
    AuthenticationService,
)

from apps.users.permissions import (
    IsAuthenticatedUser,
)


User = get_user_model()

@extend_schema(
    request=LoginSerializer,
    responses={
        200: UserMeSerializer,
        400: dict,
    },
    description="Authenticate a user and issue JWT credentials.",
)
class LoginView(APIView):
    """
    Authenticate a user and issue JWT credentials.
    """

    permission_classes = (
        AllowAny,
    )

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        tokens = AuthenticationService.login(
            user
        )

        return Response(
            {
                "user": UserMeSerializer(
                    user
                ).data,
                "tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )


class RefreshTokenView(TokenRefreshView):
    """
    Refresh an access token.

    Simple JWT handles validation and rotation
    according to project settings.
    """

    permission_classes = (
        AllowAny,
    )

@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "refresh": {
                    "type": "string",
                    "description": "JWT refresh token.",
                }
            },
            "required": ["refresh"],
        }
    },
    responses={
        205: dict,
        400: dict,
    },
    description="Blacklist the supplied refresh token.",
)
class LogoutView(APIView):
    """
    Blacklist the supplied refresh token.
    """

    permission_classes = (
        IsAuthenticatedUser,
    )

    def post(self, request):
        refresh_token = request.data.get(
            "refresh"
        )

        if not refresh_token:
            return Response(
                {
                    "detail":
                    "Refresh token is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            AuthenticationService.blacklist_refresh_token(
                refresh_token
            )

        except TokenError:
            return Response(
                {
                    "detail":
                    "Invalid or expired refresh token."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "detail":
                "Successfully logged out."
            },
            status=status.HTTP_205_RESET_CONTENT,
        )

@extend_schema(
    responses=UserMeSerializer,
    description="Return the authenticated user's profile.",
)
class MeView(APIView):
    """
    Return the authenticated user's profile.
    """

    permission_classes = (
        IsAuthenticatedUser,
    )

    def get(self, request):
        serializer = UserMeSerializer(
            request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

@extend_schema(
    request=ChangePasswordSerializer,
    responses={
        200: dict,
        400: dict,
    },
    description="Change the authenticated user's password.",
)
class ChangePasswordView(APIView):
    """
    Change the authenticated user's password.
    """

    permission_classes = (
        IsAuthenticatedUser,
    )

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        AuthenticationService.change_password(
            user=request.user,
            new_password=serializer.validated_data[
                "new_password"
            ],
        )

        return Response(
            {
                "detail":
                "Password changed successfully."
            },
            status=status.HTTP_200_OK,
        )
        