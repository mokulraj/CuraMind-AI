from django.contrib.auth import get_user_model
from django.db import transaction


User = get_user_model()


class UserService:
    """
    Business operations related to users.
    """

    @staticmethod
    @transaction.atomic
    def create_user(
        *,
        email,
        password,
        first_name="",
        last_name="",
        role=None,
    ):
        if User.objects.filter(email=email).exists():
            raise ValueError(
                "A user with this email already exists."
            )

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )

        user.set_password(password)
        user.save()

        return user

    @staticmethod
    @transaction.atomic
    def deactivate_user(*, user):
        if not user.is_active:
            return user

        user.is_active = False
        user.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return user

    @staticmethod
    @transaction.atomic
    def activate_user(*, user):
        if user.is_active:
            return user

        user.is_active = True
        user.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return user