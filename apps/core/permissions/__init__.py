"""
CuraMind AI authorization and object-permission package.
"""

from rest_framework.permissions import BasePermission

from apps.core.permissions.helpers import get_user_role


class IsOrganizationAdmin(BasePermission):
    """
    Allows access only to authenticated organization administrators.

    A user is considered an organization administrator when:

    1. The user is authenticated.
    2. The user's role is "admin", or
       the user is a Django superuser.
    """

    message = (
        "You must be an organization administrator "
        "to access this resource."
    )

    def has_permission(
        self,
        request,
        view,
    ):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        role = get_user_role(user)

        return role == "admin"