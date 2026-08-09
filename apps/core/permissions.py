from rest_framework.permissions import BasePermission


class IsOrganizationAdmin(BasePermission):
    """
    Allows organization-level administrators.
    """

    message = "Organization administrator access is required."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return (
            user.is_active
            and (
                user.is_superuser
                or getattr(user, "role", None)
            in {
                "ADMIN",
                "ORGANIZATION_ADMIN",
            }
        )
        )


class SameOrganization(BasePermission):
    """
    Object-level organization isolation.
    """

    message = "You cannot access another organization's data."

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        organization = getattr(
            obj,
            "organization",
            None,
        )

        if organization is None:
            return False

        user_organization = getattr(
            user,
            "organization",
            None,
        )

        return (
            user.is_superuser
            or (
                user_organization is not None
                and organization == user_organization
            )
        )