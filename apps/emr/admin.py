from django.contrib import admin

from .models import (
    Allergy,
    ClinicalEncounter,
    ClinicalNote,
    Diagnosis,
    MedicalRecord,
    Medication,
    VitalSign,
)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "patient__user__email",
        "patient__user__first_name",
        "patient__user__last_name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(ClinicalEncounter)
class ClinicalEncounterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "attending_doctor",
        "encounter_type",
        "status",
        "started_at",
        "completed_at",
    )

    list_filter = (
        "encounter_type",
        "status",
    )

    search_fields = (
        "patient__user__email",
        "patient__user__first_name",
        "patient__user__last_name",
        "attending_doctor__user__email",
        "attending_doctor__user__first_name",
        "attending_doctor__user__last_name",
    )

    date_hierarchy = "started_at"

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "encounter",
        "code",
        "description",
        "diagnosis_type",
        "status",
        "diagnosed_by",
        "diagnosed_at",
    )

    list_filter = (
        "diagnosis_type",
        "status",
    )

    search_fields = (
        "code",
        "description",
        "clinical_notes",
        "encounter__patient__user__email",
        "diagnosed_by__email",
    )

    date_hierarchy = "diagnosed_at"

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "allergen",
        "severity",
        "created_at",
    )

    list_filter = (
        "severity",
    )

    search_fields = (
        "allergen",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "medication_name",
        "created_at",
    )

    search_fields = (
        "medication_name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "encounter",
        "recorded_by",
        "heart_rate_bpm",
        "systolic_bp_mmhg",
        "diastolic_bp_mmhg",
        "oxygen_saturation_percent",
        "recorded_at",
    )

    list_filter = (
        "recorded_at",
    )

    search_fields = (
        "encounter__patient__user__email",
        "recorded_by__email",
    )

    date_hierarchy = "recorded_at"

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(ClinicalNote)
class ClinicalNoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "encounter",
        "author",
        "note_type",
        "is_signed",
        "signed_at",
        "created_at",
    )

    list_filter = (
        "note_type",
        "is_signed",
    )

    search_fields = (
        "encounter__patient__user__email",
        "author__email",
        "content",
    )

    date_hierarchy = "created_at"

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )