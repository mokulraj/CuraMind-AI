from rest_framework import serializers

from .models import (
    Allergy,
    ClinicalEncounter,
    ClinicalNote,
    Diagnosis,
    MedicalRecord,
    Medication,
    VitalSign,
)


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.user.full_name",
        read_only=True,
    )

    class Meta:
        model = MedicalRecord
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "patient_name",
        )


class ClinicalEncounterSerializer(
    serializers.ModelSerializer
):
    patient_name = serializers.CharField(
        source="patient.user.full_name",
        read_only=True,
    )

    doctor_name = serializers.CharField(
        source="doctor.user.full_name",
        read_only=True,
    )

    class Meta:
        model = ClinicalEncounter
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "patient_name",
            "doctor_name",
        )


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class ClinicalNoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source="created_by.full_name",
        read_only=True,
    )

    class Meta:
        model = ClinicalNote
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "created_by_name",
        )