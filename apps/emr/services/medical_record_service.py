from django.db import transaction

from apps.emr.models import (
    ClinicalEncounter,
    MedicalRecord,
)


class MedicalRecordService:
    """
    Business operations for electronic medical records.
    """

    @staticmethod
    @transaction.atomic
    def get_or_create_medical_record(
        *,
        patient,
    ):
        medical_record, _ = (
            MedicalRecord.objects.get_or_create(
                patient=patient,
            )
        )

        return medical_record

    @staticmethod
    @transaction.atomic
    def create_encounter(
        *,
        patient,
        doctor,
        **extra_fields,
    ):
        medical_record = (
            MedicalRecordService
            .get_or_create_medical_record(
                patient=patient,
            )
        )

        return ClinicalEncounter.objects.create(
            patient=patient,
            doctor=doctor,
            medical_record=medical_record,
            **extra_fields,
        )