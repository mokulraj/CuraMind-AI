from django.db import transaction

from apps.reports.models import (
    ClinicalReport,
    ReportStatus,
    ReportVersion,
)


class ReportService:
    """
    Clinical report business operations.
    """

    @staticmethod
    @transaction.atomic
    def create_report(
        *,
        patient,
        medical_record,
        author,
        report_type,
        title,
        content="",
        findings="",
        impression="",
        recommendations="",
        encounter=None,
        imaging_study=None,
        template=None,
    ):
        return ClinicalReport.objects.create(
            patient=patient,
            medical_record=medical_record,
            encounter=encounter,
            imaging_study=imaging_study,
            report_type=report_type,
            title=title,
            content=content,
            findings=findings,
            impression=impression,
            recommendations=recommendations,
            template=template,
            author=author,
        )

    @staticmethod
    @transaction.atomic
    def create_version(
        *,
        report,
        changed_by,
        title,
        content="",
        findings="",
        impression="",
        recommendations="",
        change_reason="",
    ):
        latest = (
            report.versions
            .order_by("-version_number")
            .first()
        )

        version_number = (
            latest.version_number + 1
            if latest
            else 1
        )

        return ReportVersion.objects.create(
            report=report,
            version_number=version_number,
            title=title,
            content=content,
            findings=findings,
            impression=impression,
            recommendations=recommendations,
            changed_by=changed_by,
            change_reason=change_reason,
        )

    @staticmethod
    @transaction.atomic
    def submit_for_review(
        *,
        report,
    ):
        if report.status != ReportStatus.DRAFT:
            raise ValueError(
                "Only draft reports can be submitted."
            )

        report.status = ReportStatus.IN_REVIEW

        report.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return report