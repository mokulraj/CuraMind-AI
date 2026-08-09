from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class AuthenticationService:
    """
    Authentication business logic.
    """

    @staticmethod
    def generate_tokens(user):
        refresh = RefreshToken.for_user(user)

        refresh["email"] = user.email
        refresh["role"] = getattr(
            user,
            "role",
            None,
        )

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @staticmethod
    @transaction.atomic
    def login(user):
        """
        Generate JWT credentials for an authenticated user.
        """

        user.last_login = timezone.now()

        user.save(
            update_fields=[
                "last_login",
            ]
        )

        return AuthenticationService.generate_tokens(
            user
        )

    @staticmethod
    @transaction.atomic
    def change_password(
        *,
        user,
        new_password,
    ):
        user.set_password(new_password)

        user.save(
            update_fields=[
                "password",
                "updated_at",
            ]
        )

        return user

    @staticmethod
    def blacklist_refresh_token(
        refresh_token,
    ):
        token = RefreshToken(refresh_token)
        token.blacklist()