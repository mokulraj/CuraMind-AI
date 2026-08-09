from rest_framework.viewsets import ModelViewSet

from .models import (
    Allergy,
    ClinicalEncounter,
    ClinicalNote,
    Diagnosis,
    MedicalRecord,
    Medication,
    VitalSign,
)

from .permissions import (
    CanAccessMedicalRecord,
    CanWriteClinicalData,
)

from .serializers import (
    AllergySerializer,
    ClinicalEncounterSerializer,
    ClinicalNoteSerializer,
    DiagnosisSerializer,
    MedicalRecordSerializer,
    MedicationSerializer,
    VitalSignSerializer,
)


class MedicalRecordViewSet(ModelViewSet):
    serializer_class = MedicalRecordSerializer

    permission_classes = (
        CanAccessMedicalRecord,
    )

    def get_queryset(self):
        user = self.request.user

        queryset = (
            MedicalRecord.objects
            .select_related("patient")
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

        if role in {
            "DOCTOR",
            "NURSE",
            "STAFF",
            "ADMIN",
        }:
            return queryset

        return queryset.none()

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                CanWriteClinicalData()
            ]

        return [
            CanAccessMedicalRecord()
        ]


class ClinicalEncounterViewSet(ModelViewSet):
    queryset = (
        ClinicalEncounter.objects
        .select_related(
            "patient",
            "doctor",
            "medical_record",
        )
        .all()
        .order_by("-created_at")
    )

    serializer_class = ClinicalEncounterSerializer

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                CanWriteClinicalData()
            ]

        return [
            CanAccessMedicalRecord()
        ]


class DiagnosisViewSet(ModelViewSet):
    queryset = Diagnosis.objects.all()

    serializer_class = DiagnosisSerializer

    permission_classes = (
        CanAccessMedicalRecord,
        CanWriteClinicalData,
    )


class AllergyViewSet(ModelViewSet):
    queryset = Allergy.objects.all()

    serializer_class = AllergySerializer

    permission_classes = (
        CanAccessMedicalRecord,
        CanWriteClinicalData,
    )


class MedicationViewSet(ModelViewSet):
    queryset = Medication.objects.all()

    serializer_class = MedicationSerializer

    permission_classes = (
        CanAccessMedicalRecord,
        CanWriteClinicalData,
    )


class VitalSignViewSet(ModelViewSet):
    queryset = VitalSign.objects.all()

    serializer_class = VitalSignSerializer

    permission_classes = (
        CanAccessMedicalRecord,
        CanWriteClinicalData,
    )


class ClinicalNoteViewSet(ModelViewSet):
    queryset = (
        ClinicalNote.objects
        .select_related("created_by")
        .all()
        .order_by("-created_at")
    )

    serializer_class = ClinicalNoteSerializer

    permission_classes = (
        CanAccessMedicalRecord,
        CanWriteClinicalData,
    )