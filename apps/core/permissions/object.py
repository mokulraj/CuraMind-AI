from django.core.exceptions import PermissionDenied

from apps.core.permissions.base import (
    PermissionAction,
    Resource,
)

from apps.core.permissions.helpers import (
    has_permission,
)


def is_same_user(
    user,
    target_user,
):
    if user is None:
        return False

    if target_user is None:
        return False

    return user.pk == target_user.pk


def can_access_user(
    user,
    target_user,
    action=PermissionAction.VIEW,
):
    if not has_permission(
        user,
        Resource.USER,
        action,
    ):
        return False

    if getattr(
        user,
        "is_superuser",
        False,
    ):
        return True

    return is_same_user(
        user,
        target_user,
    )


def can_access_patient(
    user,
    patient,
    action=PermissionAction.VIEW,
):
    if not has_permission(
        user,
        Resource.PATIENT,
        action,
    ):
        return False

    if getattr(
        user,
        "is_superuser",
        False,
    ):
        return True

    patient_user = getattr(
        patient,
        "user",
        None,
    )

    if is_same_user(
        user,
        patient_user,
    ):
        return True

    return is_user_related_to_patient(
        user,
        patient,
    )


def is_user_related_to_patient(
    user,
    patient,
):
    if user is None:
        return False

    if patient is None:
        return False

    user_role = getattr(
        user,
        "role",
        None,
    )

    if user_role not in {
        "doctor",
        "staff",
    }:
        return False

    doctors = getattr(
        patient,
        "doctors",
        None,
    )

    if doctors is not None:
        try:
            return doctors.filter(
                pk=user.pk
            ).exists()
        except AttributeError:
            pass

    doctor = getattr(
        patient,
        "doctor",
        None,
    )

    if doctor is not None:
        return doctor.pk == user.pk

    return False


def can_access_appointment(
    user,
    appointment,
    action=PermissionAction.VIEW,
):
    if not has_permission(
        user,
        Resource.APPOINTMENT,
        action,
    ):
        return False

    if getattr(
        user,
        "is_superuser",
        False,
    ):
        return True

    patient = getattr(
        appointment,
        "patient",
        None,
    )

    patient_user = getattr(
        patient,
        "user",
        None,
    )

    if is_same_user(
        user,
        patient_user,
    ):
        return True

    doctor = getattr(
        appointment,
        "doctor",
        None,
    )

    if is_same_user(
        user,
        doctor,
    ):
        return True

    return False


def can_access_emr(
    user,
    emr,
    action=PermissionAction.VIEW,
):
    if not has_permission(
        user,
        Resource.EMR,
        action,
    ):
        return False

    if getattr(
        user,
        "is_superuser",
        False,
    ):
        return True

    patient = getattr(
        emr,
        "patient",
        None,
    )

    if patient is None:
        return False

    return can_access_patient(
        user,
        patient,
        action=PermissionAction.VIEW,
    )


def can_access_imaging(
    user,
    imaging,
    action=PermissionAction.VIEW,
):
    if not has_permission(
        user,
        Resource.IMAGING,
        action,
    ):
        return False

    if getattr(
        user,
        "is_superuser",
        False,
    ):
        return True

    patient = getattr(
        imaging,
        "patient",
        None,
    )

    if patient is None:
        return False

    return can_access_patient(
        user,
        patient,
        action=PermissionAction.VIEW,
    )


def can_access_ai_result(
    user,
    ai_result,
    action=PermissionAction.VIEW,
):
    if not has_permission(
        user,
        Resource.AI_RESULT,
        action,
    ):
        return False

    if getattr(
        user,
        "is_superuser",
        False,
    ):
        return True

    patient = getattr(
        ai_result,
        "patient",
        None,
    )

    if patient is None:
        return False

    return can_access_patient(
        user,
        patient,
        action=PermissionAction.VIEW,
    )


def require_permission(
    user,
    resource,
    action,
):
    if not has_permission(
        user,
        resource,
        action,
    ):
        raise PermissionDenied(
            "You do not have permission to perform this action."
        )


def require_object_permission(
    allowed,
):
    if not allowed:
        raise PermissionDenied(
            "You do not have permission to access this resource."
        )

    return True