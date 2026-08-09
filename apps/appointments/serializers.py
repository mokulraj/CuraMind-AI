from rest_framework import serializers

from .models import (
    Appointment,
    AppointmentNote,
    DoctorAvailability,
)


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.user.full_name",
        read_only=True,
    )

    doctor_name = serializers.CharField(
        source="doctor.user.full_name",
        read_only=True,
    )

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "patient_name",
            "doctor_name",
        )


class DoctorAvailabilitySerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = DoctorAvailability
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class AppointmentNoteSerializer(
    serializers.ModelSerializer
):
    created_by_name = serializers.CharField(
        source="created_by.full_name",
        read_only=True,
    )

    class Meta:
        model = AppointmentNote
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "created_by_name",
        )