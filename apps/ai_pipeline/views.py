from rest_framework.viewsets import ModelViewSet

from .models import (
    AIHumanReview,
    AIInferenceJob,
    AIModel,
    AIModelVersion,
    Prediction,
)

from .permissions import (
    CanReviewAIPrediction,
    CanRunAIInference,
)

from .serializers import (
    AIHumanReviewSerializer,
    AIInferenceJobSerializer,
    AIModelSerializer,
    AIModelVersionSerializer,
    PredictionSerializer,
)


class AIModelViewSet(ModelViewSet):
    queryset = AIModel.objects.all().order_by("name")

    serializer_class = AIModelSerializer

    permission_classes = (
        CanRunAIInference,
    )


class AIModelVersionViewSet(ModelViewSet):
    queryset = (
        AIModelVersion.objects
        .select_related("model")
        .all()
        .order_by("-created_at")
    )

    serializer_class = AIModelVersionSerializer

    permission_classes = (
        CanRunAIInference,
    )


class AIInferenceJobViewSet(ModelViewSet):
    serializer_class = AIInferenceJobSerializer

    permission_classes = (
        CanRunAIInference,
    )

    def get_queryset(self):
        user = self.request.user

        queryset = (
            AIInferenceJob.objects
            .select_related(
                "model_version",
                "imaging_study",
                "requested_by",
            )
            .all()
            .order_by("-created_at")
        )

        if user.is_superuser:
            return queryset

        role = getattr(
            user,
            "role",
            None,
        )

        if role in {
            "DOCTOR",
            "RADIOLOGIST",
            "AI_ENGINEER",
            "ADMIN",
        }:
            return queryset

        return queryset.filter(
            requested_by=user
        )


class PredictionViewSet(ModelViewSet):
    queryset = (
        Prediction.objects
        .all()
        .order_by("-probability")
    )

    serializer_class = PredictionSerializer

    permission_classes = (
        CanReviewAIPrediction,
    )


class AIHumanReviewViewSet(ModelViewSet):
    queryset = (
        AIHumanReview.objects
        .all()
        .order_by("-created_at")
    )

    serializer_class = AIHumanReviewSerializer

    permission_classes = (
        CanReviewAIPrediction,
    )