from rest_framework.routers import DefaultRouter

from .views import (
    AllergyViewSet,
    ClinicalEncounterViewSet,
    ClinicalNoteViewSet,
    DiagnosisViewSet,
    MedicalRecordViewSet,
    MedicationViewSet,
    VitalSignViewSet,
)


app_name = "emr"


router = DefaultRouter()

router.register(
    "medical-records",
    MedicalRecordViewSet,
    basename="medical-record",
)

router.register(
    "encounters",
    ClinicalEncounterViewSet,
    basename="encounter",
)

router.register(
    "diagnoses",
    DiagnosisViewSet,
    basename="diagnosis",
)

router.register(
    "allergies",
    AllergyViewSet,
    basename="allergy",
)

router.register(
    "medications",
    MedicationViewSet,
    basename="medication",
)

router.register(
    "vital-signs",
    VitalSignViewSet,
    basename="vital-sign",
)

router.register(
    "clinical-notes",
    ClinicalNoteViewSet,
    basename="clinical-note",
)


urlpatterns = router.urls