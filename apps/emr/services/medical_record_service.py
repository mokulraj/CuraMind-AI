from django.db import transaction
from django.utils import timezone

from apps.emr.models import (
    Allergy,
    ClinicalEncounter,
    ClinicalNote,
    Diagnosis,
    MedicalRecord,
    Medication,
    VitalSign,
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
            attending_doctor,
            **extra_fields,
        ):
            """
            Create a clinical encounter for a patient.

            The encounter is always linked to the patient's
            medical record.
            """

            medical_record = (
                MedicalRecordService
                .get_or_create_medical_record(
                    patient=patient,
                )
            )

            encounter = ClinicalEncounter(
                patient=patient,
                attending_doctor=attending_doctor,
                medical_record=medical_record,
                started_at=timezone.now(),
                **extra_fields,
            )

            encounter.full_clean()
            encounter.save()

            return encounter
        
    @staticmethod
    @transaction.atomic
    def complete_encounter(
        *,
        encounter,
    ):
        """
        Complete an open clinical encounter.

        The encounter receives a completion timestamp
        when its status changes to COMPLETED.
        """

        if encounter.status == "COMPLETED":
            raise ValueError(
                "Clinical encounter is already completed."
            )

        encounter.status = "COMPLETED"
        encounter.completed_at = timezone.now()

        encounter.save(
            update_fields=[
                "status",
                "completed_at",
                "updated_at",
            ]
        )

        return encounter

    @staticmethod
    @transaction.atomic
    def update_encounter(
        *,
        encounter,
        chief_complaint=None,
        history_of_present_illness=None,
        clinical_summary=None,
        examination_notes=None,
        treatment_plan=None,
    ):
        """
        Update clinical information for an encounter.

        Completed encounters cannot be modified.
        """

        if encounter.completed_at is not None:
            raise ValueError(
                "Completed clinical encounters cannot be modified."
            )

        fields_to_update = {
            "chief_complaint": chief_complaint,
            "history_of_present_illness": (
                history_of_present_illness
            ),
            "clinical_summary": clinical_summary,
            "examination_notes": examination_notes,
            "treatment_plan": treatment_plan,
        }

        updated_fields = []

        for field_name, value in fields_to_update.items():
            if value is not None:
                setattr(
                    encounter,
                    field_name,
                    value,
                )
                updated_fields.append(field_name)

        if updated_fields:
            encounter.save(
                update_fields=updated_fields
            )

        return encounter
    
    
    @staticmethod
    @transaction.atomic
    def record_vital_signs(
            *,
            encounter,
            recorded_by,
            temperature_celsius=None,
            heart_rate_bpm=None,
            respiratory_rate_bpm=None,
            systolic_bp_mmhg=None,
            diastolic_bp_mmhg=None,
            oxygen_saturation_percent=None,
            weight_kg=None,
            height_cm=None,
            notes="",
        ):
            """
            Record a set of vital signs for a clinical encounter.

            At least one vital sign must be provided.
            """

            vital_sign = VitalSign(
                encounter=encounter,
                recorded_by=recorded_by,
                temperature_celsius=temperature_celsius,
                heart_rate_bpm=heart_rate_bpm,
                respiratory_rate_bpm=respiratory_rate_bpm,
                systolic_bp_mmhg=systolic_bp_mmhg,
                diastolic_bp_mmhg=diastolic_bp_mmhg,
                oxygen_saturation_percent=(
                    oxygen_saturation_percent
                ),
                weight_kg=weight_kg,
                height_cm=height_cm,
                recorded_at=timezone.now(),
                notes=notes,
            )

            vital_sign.full_clean()
            vital_sign.save()

            return vital_sign
        
        
    @staticmethod
    @transaction.atomic
    def create_diagnosis(
        *,
        encounter,
        code,
        description,
        diagnosis_type="PRIMARY",
        status="ACTIVE",
        clinical_notes="",
    ):
        """
        Create a diagnosis for a clinical encounter.

        The diagnosing doctor is always the encounter's
        attending doctor.
        """

        return Diagnosis.objects.create(
            encounter=encounter,
            code=code,
            description=description,
            diagnosis_type=diagnosis_type,
            status=status,
            clinical_notes=clinical_notes,
            diagnosed_by=encounter.attending_doctor,
            diagnosed_at=timezone.now(),
        )
        
    @staticmethod
    @transaction.atomic
    def resolve_diagnosis(
        *,
        diagnosis,
    ):
        """
        Mark an active diagnosis as resolved.
        """

        if diagnosis.status == "RESOLVED":
            raise ValueError(
                "Diagnosis is already resolved."
            )

        diagnosis.status = "RESOLVED"

        diagnosis.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return diagnosis
        
    @staticmethod
    @transaction.atomic
    def create_allergy(
        *,
        patient,
        recorded_by,
        allergen,
        reaction="",
        severity="MILD",
        status="ACTIVE",
        notes="",
    ):
        medical_record = (
            MedicalRecordService
            .get_or_create_medical_record(
                patient=patient,
            )
        )

        return Allergy.objects.create(
            medical_record=medical_record,
            allergen=allergen,
            reaction=reaction,
            severity=severity,
            status=status,
            notes=notes,
            recorded_by=recorded_by,
        )
        
    @staticmethod
    def get_medical_record_summary(
        *,
        medical_record,
    ):
        """
        Return a complete summary of a medical record.
        """

        encounters = (
            ClinicalEncounter.objects
            .filter(
                medical_record=medical_record,
                is_deleted=False,
                is_active=True,
            )
            .select_related(
                "patient__user",
                "attending_doctor__user",
            )
            .order_by(
                "-started_at",
            )
        )

        diagnoses = (
            Diagnosis.objects
            .filter(
                encounter__medical_record=medical_record,
                is_deleted=False,
                is_active=True,
            )
            .select_related(
                "encounter",
                "diagnosed_by__user",
            )
            .order_by(
                "-diagnosed_at",
            )
        )

        allergies = (
            Allergy.objects
            .filter(
                medical_record=medical_record,
                is_deleted=False,
                is_active=True,
            )
            .select_related(
                "recorded_by__user",
            )
            .order_by(
                "allergen",
            )
        )

        medications = (
            Medication.objects
            .filter(
                medical_record=medical_record,
                is_deleted=False,
                is_active=True,
            )
            .select_related(
                "encounter",
                "prescribed_by__user",
            )
            .order_by(
                "-prescribed_at",
            )
        )


    @staticmethod
    @transaction.atomic
    def create_medication(
        *,
        patient,
        encounter,
        prescribed_by,
        medication_name,
        dosage,
        route,
        frequency,
        generic_name="",
        duration="",
        instructions="",
        status="ACTIVE",
        prescribed_at=None,
        discontinued_at=None,
    ):
        medical_record = (
            MedicalRecordService
            .get_or_create_medical_record(
                patient=patient,
            )
        )

        if encounter.patient_id != patient.id:
            raise ValueError(
                "Medication patient must match encounter patient."
            )

        if (
            prescribed_by.id
            != encounter.attending_doctor_id
        ):
            raise ValueError(
                "The prescribing doctor must be "
                "the attending doctor."
            )

        if prescribed_at is None:
            prescribed_at = timezone.now()

        return Medication.objects.create(
            medical_record=medical_record,
            encounter=encounter,
            medication_name=medication_name,
            generic_name=generic_name,
            dosage=dosage,
            route=route,
            frequency=frequency,
            duration=duration,
            instructions=instructions,
            status=status,
            prescribed_by=prescribed_by,
            prescribed_at=prescribed_at,
            discontinued_at=discontinued_at,
        )
        
    @staticmethod
    @transaction.atomic
    def discontinue_medication(
        *,
        medication,
    ):
        """
        Discontinue an active medication.

        A discontinued medication receives a
        discontinuation timestamp.
        """

        if medication.status == "DISCONTINUED":
            raise ValueError(
                "Medication is already discontinued."
            )

        medication.status = "DISCONTINUED"
        medication.discontinued_at = timezone.now()

        medication.save(
            update_fields=[
                "status",
                "discontinued_at",
                "updated_at",
            ]
        )

        return medication
        
    @staticmethod
    @transaction.atomic
    def create_clinical_note(
        *,
        encounter,
        author,
        note_type="PROGRESS",
        content="",
        is_signed=False,
    ):
        """
        Create a clinical note for a clinical encounter.

        A signed note receives the current timestamp.
        An unsigned note does not have a signed timestamp.
        """

        signed_at = (
            timezone.now()
            if is_signed
            else None
        )

        return ClinicalNote.objects.create(
            encounter=encounter,
            author=author,
            note_type=note_type,
            content=content,
            is_signed=is_signed,
            signed_at=signed_at,
        )
        
    @staticmethod
    @transaction.atomic
    def sign_clinical_note(
        *,
        note,
    ):
        """
        Sign an existing clinical note.

        A signed clinical note receives the current timestamp.
        An already signed note cannot be signed again.
        """

        if note.is_signed:
            raise ValueError(
                "Clinical note is already signed."
            )

        note.is_signed = True
        note.signed_at = timezone.now()

        note.save(
            update_fields=[
                "is_signed",
                "signed_at",
                "updated_at",
            ]
        )

        return note
    
    @staticmethod
    def get_medical_record_summary(
        *,
        medical_record,
    ):
        """
        Return a complete summary of a medical record.
        """

        encounters = (
            ClinicalEncounter.objects
            .filter(
                medical_record=medical_record,
                is_deleted=False,
                is_active=True,
            )
            .select_related(
                "patient__user",
                "attending_doctor__user",
            )
            .order_by(
                "-started_at",
            )
        )

        diagnoses = (
            Diagnosis.objects
            .filter(
                encounter__medical_record=medical_record,
                is_deleted=False,
                is_active=True,
            )
            .select_related(
                "encounter",
                "diagnosed_by__user",
            )
            .order_by(
                "-diagnosed_at",
            )
        )

        allergies = (
            Allergy.objects
            .filter(
                medical_record=medical_record,
                is_deleted=False,
                is_active=True,
            )
            .select_related(
                "recorded_by__user",
            )
            .order_by(
                "allergen",
            )
        )

        medications = (
            Medication.objects
            .filter(
                medical_record=medical_record,
                is_deleted=False,
                is_active=True,
            )
            .select_related(
                "encounter",
                "prescribed_by__user",
            )
            .order_by(
                "-prescribed_at",
            )
        )

        vital_signs = (
            VitalSign.objects
            .filter(
                encounter__medical_record=medical_record,
                is_deleted=False,
                is_active=True,
            )
            .select_related(
                "encounter",
                "recorded_by",
            )
            .order_by(
                "-recorded_at",
            )
        )

        clinical_notes = (
            ClinicalNote.objects
            .filter(
                encounter__medical_record=medical_record,
                is_deleted=False,
                is_active=True,
            )
            .select_related(
                "encounter",
                "author",
            )
            .order_by(
                "-created_at",
            )
        )

        return {
            "medical_record": medical_record,
            "patient": medical_record.patient,
            "encounters": encounters,
            "diagnoses": diagnoses,
            "allergies": allergies,
            "medications": medications,
            "vital_signs": vital_signs,
            "clinical_notes": clinical_notes,
        }