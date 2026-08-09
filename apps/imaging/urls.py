from rest_framework.routers import DefaultRouter

from .views import (
    DICOMInstanceViewSet,
    ImagingAIProcessingViewSet,
    ImagingSeriesViewSet,
    ImagingStudyViewSet,
    RadiologyReportViewSet,
)


app_name = "imaging"


router = DefaultRouter()

router.register(
    "studies",
    ImagingStudyViewSet,
    basename="study",
)

router.register(
    "series",
    ImagingSeriesViewSet,
    basename="series",
)

router.register(
    "dicom-instances",
    DICOMInstanceViewSet,
    basename="dicom-instance",
)

router.register(
    "radiology-reports",
    RadiologyReportViewSet,
    basename="radiology-report",
)

router.register(
    "ai-processing",
    ImagingAIProcessingViewSet,
    basename="ai-processing",
)


urlpatterns = router.urls