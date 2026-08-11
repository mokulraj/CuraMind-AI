class PermissionAction:
    VIEW = "view"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    PROCESS = "process"


class Resource:
    USER = "user"
    PATIENT = "patient"
    APPOINTMENT = "appointment"
    EMR = "emr"
    IMAGING = "imaging"
    AI_RESULT = "ai_result"
    REPORT = "report"
    PAYMENT = "payment"
    NOTIFICATION = "notification"
    AUDIT = "audit"