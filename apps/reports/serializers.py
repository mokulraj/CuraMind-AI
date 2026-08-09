from rest_framework import serializers

from .models import (
    ClinicalReport,
    GeneratedReport,
    ReportExport,
    ReportTemplate,
    ReportVersion,
)


class ReportTemplateSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = ReportTemplate
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class ReportVersionSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = ReportVersion
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class ClinicalReportSerializer(
    serializers.ModelSerializer
):
    versions = ReportVersionSerializer(
        many=True,
        read_only=True,
    )

    patient_name = serializers.CharField(
        source="patient.user.full_name",
        read_only=True,
    )

    class Meta:
        model = ClinicalReport
        fields = "__all__"
        read_only_fields = (
            "id",
            "report_number",
            "created_at",
            "updated_at",
            "versions",
            "patient_name",
        )


class GeneratedReportSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = GeneratedReport
        fields = "__all__"
        read_only_fields = (
            "id",
            "storage_key",
            "checksum_sha256",
            "generated_at",
            "created_at",
            "updated_at",
        )


class ReportExportSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = ReportExport
        fields = "__all__"
        read_only_fields = (
            "id",
            "status",
            "celery_task_id",
            "storage_key",
            "failure_reason",
            "requested_at",
            "completed_at",
            "created_at",
            "updated_at",
        )