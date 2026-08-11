from apps.core.permissions.roles import (
    ROLE_PERMISSIONS,
)


def get_user_role(
    user,
):
    if user is None:
        return None

    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return "admin"

    return getattr(
        user,
        "role",
        None,
    )


def has_permission(
    user,
    resource,
    action,
):
    role = get_user_role(
        user
    )

    if role is None:
        return False

    role_permissions = (
        ROLE_PERMISSIONS.get(
            role,
            {},
        )
    )

    resource_permissions = (
        role_permissions.get(
            resource,
            set(),
        )
    )

    return action in resource_permissions


def has_any_permission(
    user,
    resource,
    actions,
):
    return any(
        has_permission(
            user,
            resource,
            action,
        )
        for action in actions
    )


def has_all_permissions(
    user,
    resource,
    actions,
):
    return all(
        has_permission(
            user,
            resource,
            action,
        )
        for action in actions
    )