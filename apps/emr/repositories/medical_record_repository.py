from apps.emr.models import (
    ClinicalEncounter,
    MedicalRecord,
)


class MedicalRecordRepository:
    """
    Database access for electronic medical records.
    """

    @staticmethod
    def get_by_id(
        medical_record_id,
    ):
        return (
            MedicalRecord.objects
            .select_related(
                "patient",
            )
            .filter(pk=medical_record_id)
            .first()
        )

    @staticmethod
    def get_by_patient(
        patient_id,
    ):
        return (
            MedicalRecord.objects
            .select_related(
                "patient",
            )
            .filter(
                patient_id=patient_id
            )
            .first()
        )

    @staticmethod
    def list_encounters(
        *,
        patient_id=None,
        doctor_id=None,
    ):
        queryset = (
            ClinicalEncounter.objects
            .select_related(
                "patient",
                "doctor",
                "medical_record",
            )
        )

        if patient_id:
            queryset = queryset.filter(
                patient_id=patient_id
            )

        if doctor_id:
            queryset = queryset.filter(
                doctor_id=doctor_id
            )

        return queryset.order_by(
            "-created_at"
        )

    @staticmethod
    def get_encounter_by_id(
        encounter_id,
    ):
        return (
            ClinicalEncounter.objects
            .select_related(
                "patient",
                "doctor",
                "medical_record",
            )
            .filter(pk=encounter_id)
            .first()
        )