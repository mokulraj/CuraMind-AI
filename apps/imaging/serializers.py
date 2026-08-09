from rest_framework import serializers

from .models import (
    DICOMInstance,
    ImagingAIProcessing,
    ImagingSeries,
    ImagingStudy,
    RadiologyReport,
)


class ImagingStudySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.user.full_name",
        read_only=True,
    )

    doctor_name = serializers.CharField(
        source="ordered_by.user.full_name",
        read_only=True,
    )

    class Meta:
        model = ImagingStudy
        fields = "__all__"
        read_only_fields = (
            "id",
            "study_instance_uid",
            "accession_number",
            "created_at",
            "updated_at",
            "patient_name",
            "doctor_name",
        )


class ImagingSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagingSeries
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class DICOMInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DICOMInstance
        fields = "__all__"
        read_only_fields = (
            "id",
            "sop_instance_uid",
            "created_at",
            "updated_at",
        )


class RadiologyReportSerializer(
    serializers.ModelSerializer
):
    radiologist_name = serializers.CharField(
        source="radiologist.user.full_name",
        read_only=True,
    )

    class Meta:
        model = RadiologyReport
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "radiologist_name",
        )


class ImagingAIProcessingSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = ImagingAIProcessing
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )