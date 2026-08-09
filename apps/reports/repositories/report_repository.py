from apps.reports.models import (
    ClinicalReport,
    GeneratedReport,
    ReportExport,
    ReportTemplate,
    ReportVersion,
)


class ReportRepository:
    """
    Database access for clinical reports.
    """

    @staticmethod
    def get_report_by_id(
        report_id,
    ):
        return (
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
            .filter(pk=report_id)
            .first()
        )

    @staticmethod
    def list_patient_reports(
        patient_id,
    ):
        return (
            ClinicalReport.objects
            .select_related(
                "patient",
                "author",
                "reviewer",
                "signed_by",
            )
            .filter(
                patient_id=patient_id
            )
            .order_by("-created_at")
        )

    @staticmethod
    def list_reports_by_status(
        status,
    ):
        return (
            ClinicalReport.objects
            .select_related(
                "patient",
                "author",
                "reviewer",
            )
            .filter(
                status=status
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_latest_version(
        report_id,
    ):
        return (
            ReportVersion.objects
            .filter(
                report_id=report_id
            )
            .order_by("-version_number")
            .first()
        )

    @staticmethod
    def list_generated_artifacts(
        report_id,
    ):
        return (
            GeneratedReport.objects
            .filter(
                report_id=report_id
            )
            .order_by("-generated_at")
        )

    @staticmethod
    def list_exports(
        report_id,
    ):
        return (
            ReportExport.objects
            .filter(
                report_id=report_id
            )
            .order_by("-requested_at")
        )

    @staticmethod
    def list_active_templates(
        report_type=None,
    ):
        queryset = ReportTemplate.objects.filter(
            is_active=True
        )

        if report_type:
            queryset = queryset.filter(
                report_type=report_type
            )

        return queryset.order_by("name")