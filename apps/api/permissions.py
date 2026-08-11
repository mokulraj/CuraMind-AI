from rest_framework.permissions import (
    BasePermission,
)

from apps.core.permissions.base import (
    PermissionAction,
    Resource,
)

from apps.core.permissions.helpers import (
    has_permission,
)

from apps.core.permissions.object import (
    can_access_appointment,
    can_access_ai_result,
    can_access_emr,
    can_access_imaging,
    can_access_patient,
)


class IsAuthenticatedAndActive(
    BasePermission
):
    message = (
        "Authentication is required."
    )

    def has_permission(
        self,
        request,
        view,
    ):
        user = request.user

        return (
            user is not None
            and user.is_authenticated
            and user.is_active
        )


class HasResourcePermission(
    BasePermission
):
    resource = None

    action_map = {
        "GET": PermissionAction.VIEW,
        "POST": PermissionAction.CREATE,
        "PUT": PermissionAction.UPDATE,
        "PATCH": PermissionAction.UPDATE,
        "DELETE": PermissionAction.DELETE,
    }

    def get_action(
        self,
        request,
    ):
        return self.action_map.get(
            request.method
        )

    def has_permission(
        self,
        request,
        view,
    ):
        if not (
            request.user
            and request.user.is_authenticated
        ):
            return False

        action = self.get_action(
            request
        )

        if action is None:
            return False

        return has_permission(
            request.user,
            self.resource,
            action,
        )


class CanAccessPatient(
    IsAuthenticatedAndActive
):
    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        action = {
            "GET": PermissionAction.VIEW,
            "PUT": PermissionAction.UPDATE,
            "PATCH": PermissionAction.UPDATE,
            "DELETE": PermissionAction.DELETE,
        }.get(
            request.method
        )

        if action is None:
            return False

        return can_access_patient(
            request.user,
            obj,
            action,
        )


class CanAccessAppointment(
    IsAuthenticatedAndActive
):
    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        action = {
            "GET": PermissionAction.VIEW,
            "PUT": PermissionAction.UPDATE,
            "PATCH": PermissionAction.UPDATE,
            "DELETE": PermissionAction.DELETE,
        }.get(
            request.method
        )

        if action is None:
            return False

        return can_access_appointment(
            request.user,
            obj,
            action,
        )


class CanAccessEMR(
    IsAuthenticatedAndActive
):
    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        action = {
            "GET": PermissionAction.VIEW,
            "PUT": PermissionAction.UPDATE,
            "PATCH": PermissionAction.UPDATE,
            "DELETE": PermissionAction.DELETE,
        }.get(
            request.method
        )

        if action is None:
            return False

        return can_access_emr(
            request.user,
            obj,
            action,
        )


class CanAccessImaging(
    IsAuthenticatedAndActive
):
    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        action = {
            "GET": PermissionAction.VIEW,
            "PUT": PermissionAction.UPDATE,
            "PATCH": PermissionAction.UPDATE,
            "DELETE": PermissionAction.DELETE,
        }.get(
            request.method
        )

        if action is None:
            return False

        return can_access_imaging(
            request.user,
            obj,
            action,
        )


class CanAccessAIResult(
    IsAuthenticatedAndActive
):
    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        action = {
            "GET": PermissionAction.VIEW,
        }.get(
            request.method
        )

        if action is None:
            return False

        return can_access_ai_result(
            request.user,
            obj,
            action,
        )


class CanViewAuditLogs(
    IsAuthenticatedAndActive
):
    def has_permission(
        self,
        request,
        view,
    ):
        if not super().has_permission(
            request,
            view,
        ):
            return False

        return has_permission(
            request.user,
            Resource.AUDIT,
            PermissionAction.VIEW,
        )