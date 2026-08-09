from rest_framework.permissions import BasePermission


class IsAuthenticatedUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    message = "Authentication is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )


class IsAdminUser(BasePermission):
    """
    Allows access to platform administrators.
    """

    message = "Administrator access is required."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and (
                user.is_superuser
                or getattr(user, "is_staff", False)
            )
        )


class IsDoctor(BasePermission):
    """
    Allows access to users with doctor role.
    """

    message = "Doctor access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and getattr(request.user, "role", None)
            == "DOCTOR"
        )


class IsPatient(BasePermission):
    """
    Allows access to users with patient role.
    """

    message = "Patient access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and getattr(request.user, "role", None)
            == "PATIENT"
        )


class IsStaffMember(BasePermission):
    """
    Allows healthcare staff access.
    """

    message = "Healthcare staff access is required."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and getattr(user, "role", None)
            in {
                "STAFF",
                "NURSE",
                "RECEPTIONIST",
                "ADMIN",
            }
        )


class IsDoctorOrStaff(BasePermission):
    """
    Allows doctors and authorized healthcare staff.
    """

    message = "Doctor or healthcare staff access is required."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        role = getattr(user, "role", None)

        return (
            user.is_active
            and role in {
                "DOCTOR",
                "STAFF",
                "NURSE",
                "ADMIN",
            }
        )


class IsOwner(BasePermission):
    """
    Object-level ownership permission.

    The object must expose either:
        user
    or:
        owner
    """

    message = "You do not have permission to access this resource."

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        owner = getattr(obj, "user", None)

        if owner is None:
            owner = getattr(obj, "owner", None)

        return owner == user