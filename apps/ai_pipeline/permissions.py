from rest_framework.permissions import BasePermission


class CanRunAIInference(BasePermission):
    """
    Controls creation of clinical AI inference jobs.
    """

    message = "You do not have permission to run AI inference."

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
                    "DOCTOR",
                    "RADIOLOGIST",
                    "AI_ENGINEER",
                    "ADMIN",
                }
            )
        )


class CanReviewAIPrediction(BasePermission):
    """
    Human clinical review of AI output.
    """

    message = "Clinical AI review access is required."

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
                    "DOCTOR",
                    "RADIOLOGIST",
                    "ADMIN",
                }
            )
        )