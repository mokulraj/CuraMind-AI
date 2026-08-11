from apps.core.permissions.base import (
    PermissionAction,
    Resource,
)


ROLE_PERMISSIONS = {
    "admin": {
        Resource.USER: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.DELETE,
        },
        Resource.PATIENT: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        },
        Resource.APPOINTMENT: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.DELETE,
            PermissionAction.APPROVE,
            PermissionAction.REJECT,
        },
        Resource.EMR: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        },
        Resource.IMAGING: {
            PermissionAction.VIEW,
            PermissionAction.UPLOAD,
            PermissionAction.DOWNLOAD,
            PermissionAction.PROCESS,
        },
        Resource.AI_RESULT: {
            PermissionAction.VIEW,
            PermissionAction.PROCESS,
        },
        Resource.REPORT: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.DOWNLOAD,
        },
        Resource.PAYMENT: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        },
        Resource.NOTIFICATION: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
        },
        Resource.AUDIT: {
            PermissionAction.VIEW,
        },
    },

    "doctor": {
        Resource.PATIENT: {
            PermissionAction.VIEW,
        },
        Resource.APPOINTMENT: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.APPROVE,
            PermissionAction.REJECT,
        },
        Resource.EMR: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        },
        Resource.IMAGING: {
            PermissionAction.VIEW,
            PermissionAction.UPLOAD,
            PermissionAction.DOWNLOAD,
            PermissionAction.PROCESS,
        },
        Resource.AI_RESULT: {
            PermissionAction.VIEW,
            PermissionAction.PROCESS,
        },
        Resource.REPORT: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.DOWNLOAD,
        },
        Resource.NOTIFICATION: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
        },
    },

    "patient": {
        Resource.PATIENT: {
            PermissionAction.VIEW,
            PermissionAction.UPDATE,
        },
        Resource.APPOINTMENT: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        },
        Resource.EMR: {
            PermissionAction.VIEW,
        },
        Resource.IMAGING: {
            PermissionAction.VIEW,
            PermissionAction.DOWNLOAD,
        },
        Resource.AI_RESULT: {
            PermissionAction.VIEW,
        },
        Resource.REPORT: {
            PermissionAction.VIEW,
            PermissionAction.DOWNLOAD,
        },
        Resource.PAYMENT: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
        },
        Resource.NOTIFICATION: {
            PermissionAction.VIEW,
        },
    },

    "staff": {
        Resource.PATIENT: {
            PermissionAction.VIEW,
        },
        Resource.APPOINTMENT: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
        },
        Resource.EMR: {
            PermissionAction.VIEW,
        },
        Resource.IMAGING: {
            PermissionAction.VIEW,
            PermissionAction.UPLOAD,
        },
        Resource.REPORT: {
            PermissionAction.VIEW,
        },
        Resource.NOTIFICATION: {
            PermissionAction.VIEW,
            PermissionAction.CREATE,
        },
    },
}