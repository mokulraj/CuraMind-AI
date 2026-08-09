from rest_framework.routers import DefaultRouter

from .views import (
    AIHumanReviewViewSet,
    AIInferenceJobViewSet,
    AIModelVersionViewSet,
    AIModelViewSet,
    PredictionViewSet,
)


app_name = "ai-pipeline"


router = DefaultRouter()

router.register(
    "models",
    AIModelViewSet,
    basename="model",
)

router.register(
    "model-versions",
    AIModelVersionViewSet,
    basename="model-version",
)

router.register(
    "inference-jobs",
    AIInferenceJobViewSet,
    basename="inference-job",
)

router.register(
    "predictions",
    PredictionViewSet,
    basename="prediction",
)

router.register(
    "human-reviews",
    AIHumanReviewViewSet,
    basename="human-review",
)


urlpatterns = router.urls