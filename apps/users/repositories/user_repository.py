from django.contrib.auth import get_user_model


User = get_user_model()


class UserRepository:
    """
    Database access for users.
    """

    @staticmethod
    def get_by_id(user_id):
        return (
            User.objects
            .filter(pk=user_id)
            .first()
        )

    @staticmethod
    def get_by_email(email):
        return (
            User.objects
            .filter(email__iexact=email)
            .first()
        )

    @staticmethod
    def exists_by_email(email):
        return User.objects.filter(
            email__iexact=email
        ).exists()

    @staticmethod
    def list_active():
        return (
            User.objects
            .filter(is_active=True)
            .order_by("email")
        )

    @staticmethod
    def list_by_role(role):
        return (
            User.objects
            .filter(
                role=role,
                is_active=True,
            )
            .order_by("email")
        )