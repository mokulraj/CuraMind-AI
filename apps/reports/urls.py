from rest_framework.routers import DefaultRouter

from .views import (
    ClinicalReportViewSet,
    GeneratedReportViewSet,
    ReportExportViewSet,
    ReportTemplateViewSet,
    ReportVersionViewSet,
)


app_name = "reports"


router = DefaultRouter()

router.register(
    "clinical-reports",
    ClinicalReportViewSet,
    basename="clinical-report",
)

router.register(
    "versions",
    ReportVersionViewSet,
    basename="version",
)

router.register(
    "templates",
    ReportTemplateViewSet,
    basename="template",
)

router.register(
    "generated-reports",
    GeneratedReportViewSet,
    basename="generated-report",
)

router.register(
    "exports",
    ReportExportViewSet,
    basename="export",
)


urlpatterns = router.urls