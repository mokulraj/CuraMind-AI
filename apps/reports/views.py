from rest_framework.viewsets import ModelViewSet

from .models import (
    ClinicalReport,
    GeneratedReport,
    ReportExport,
    ReportTemplate,
    ReportVersion,
)

from .permissions import (
    CanAccessClinicalReports,
    CanCreateClinicalReport,
    CanSignClinicalReport,
)

from .serializers import (
    ClinicalReportSerializer,
    GeneratedReportSerializer,
    ReportExportSerializer,
    ReportTemplateSerializer,
    ReportVersionSerializer,
)


class ClinicalReportViewSet(ModelViewSet):
    serializer_class = ClinicalReportSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = (
            ClinicalReport.objects
            .select_related(
                "patient",
                "medical_record",
                "encounter",
                "imaging_study",
                "template",
                "author",
                "reviewer",
                "signed_by",
            )
            .prefetch_related("versions")
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
            "NURSE",
            "STAFF",
            "ADMIN",
        }:
            return queryset

        if role == "PATIENT":
            patient = getattr(
                user,
                "patient_profile",
                None,
            )

            if patient:
                return queryset.filter(
                    patient=patient
                )

        return queryset.none()

    def get_permissions(self):
        if self.action == "create":
            return [
                CanCreateClinicalReport()
            ]

        if self.action in {
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                CanCreateClinicalReport()
            ]

        return [
            CanAccessClinicalReports()
        ]


class ReportVersionViewSet(ModelViewSet):
    queryset = (
        ReportVersion.objects
        .select_related(
            "report",
            "changed_by",
        )
        .all()
        .order_by(
            "report_id",
            "-version_number",
        )
    )

    serializer_class = ReportVersionSerializer

    permission_classes = (
        CanAccessClinicalReports,
    )


class ReportTemplateViewSet(ModelViewSet):
    queryset = (
        ReportTemplate.objects
        .all()
        .order_by("name")
    )

    serializer_class = ReportTemplateSerializer

    permission_classes = (
        CanCreateClinicalReport,
    )


class GeneratedReportViewSet(ModelViewSet):
    queryset = (
        GeneratedReport.objects
        .all()
        .order_by("-generated_at")
    )

    serializer_class = GeneratedReportSerializer

    permission_classes = (
        CanAccessClinicalReports,
    )


class ReportExportViewSet(ModelViewSet):
    queryset = (
        ReportExport.objects
        .all()
        .order_by("-requested_at")
    )

    serializer_class = ReportExportSerializer

    permission_classes = (
        CanAccessClinicalReports,
    )