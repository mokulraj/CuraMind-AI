from django.contrib import admin

from .models import (
    DICOMInstance,
    ImagingAIProcessing,
    ImagingSeries,
    ImagingStudy,
    RadiologyReport,
)


@admin.register(ImagingStudy)
class ImagingStudyAdmin(admin.ModelAdmin):
    list_display = (
        "accession_number",
        "patient",
        "modality",
        "body_part",
        "status",
        "priority",
        "requested_at",
    )
    list_filter = (
        "modality",
        "status",
        "priority",
    )
    search_fields = (
        "accession_number",
        "study_instance_uid",
        "patient__user__email",
        "patient__user__first_name",
        "patient__user__last_name",
    )
    date_hierarchy = "requested_at"
    readonly_fields = (
        "id",
        "study_instance_uid",
        "accession_number",
        "created_at",
        "updated_at",
    )


@admin.register(ImagingSeries)
class ImagingSeriesAdmin(admin.ModelAdmin):
    list_display = (
        "series_instance_uid",
        "study",
        "series_number",
        "modality",
        "number_of_instances",
    )
    list_filter = (
        "modality",
    )
    search_fields = (
        "series_instance_uid",
        "study__accession_number",
    )
    readonly_fields = (
        "id",
        "series_instance_uid",
        "created_at",
        "updated_at",
    )


@admin.register(DICOMInstance)
class DICOMInstanceAdmin(admin.ModelAdmin):
    list_display = (
        "sop_instance_uid",
        "series",
        "instance_number",
        "file_size_bytes",
    )
    search_fields = (
        "sop_instance_uid",
        "storage_key",
        "series__series_instance_uid",
    )
    readonly_fields = (
        "id",
        "sop_instance_uid",
        "storage_key",
        "created_at",
        "updated_at",
    )


@admin.register(RadiologyReport)
class RadiologyReportAdmin(admin.ModelAdmin):
    list_display = (
        "study",
        "radiologist",
        "status",
        "signed_at",
    )
    list_filter = (
        "status",
    )
    search_fields = (
        "study__accession_number",
        "radiologist__user__email",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(ImagingAIProcessing)
class ImagingAIProcessingAdmin(admin.ModelAdmin):
    list_display = (
        "study",
        "model_name",
        "model_version",
        "status",
        "confidence_score",
        "created_at",
    )
    list_filter = (
        "status",
    )
    search_fields = (
        "study__accession_number",
        "model_name",
        "model_version",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )