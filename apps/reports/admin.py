from django.contrib import admin

from .models import (
    ClinicalReport,
    GeneratedReport,
    ReportExport,
    ReportTemplate,
    ReportVersion,
)


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "report_type",
        "version",
        "is_active",
        "created_by",
    )
    list_filter = (
        "report_type",
        "is_active",
    )
    search_fields = (
        "name",
        "description",
        "created_by__email",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


class ReportVersionInline(admin.TabularInline):
    model = ReportVersion
    extra = 0
    readonly_fields = (
        "version_number",
        "changed_by",
        "created_at",
    )


@admin.register(ClinicalReport)
class ClinicalReportAdmin(admin.ModelAdmin):
    list_display = (
        "report_number",
        "patient",
        "report_type",
        "status",
        "author",
        "reviewer",
        "signed_by",
        "created_at",
    )
    list_filter = (
        "report_type",
        "status",
    )
    search_fields = (
        "report_number",
        "title",
        "patient__user__email",
        "author__email",
        "reviewer__email",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "id",
        "report_number",
        "created_at",
        "updated_at",
    )
    inlines = [
        ReportVersionInline,
    ]


@admin.register(ReportVersion)
class ReportVersionAdmin(admin.ModelAdmin):
    list_display = (
        "report",
        "version_number",
        "changed_by",
        "created_at",
    )
    search_fields = (
        "report__report_number",
        "changed_by__email",
        "change_reason",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = (
        "report",
        "format",
        "file_name",
        "content_type",
        "file_size_bytes",
        "generated_at",
    )
    list_filter = (
        "format",
        "content_type",
    )
    search_fields = (
        "report__report_number",
        "file_name",
        "storage_key",
        "checksum_sha256",
    )
    readonly_fields = (
        "id",
        "storage_key",
        "checksum_sha256",
        "generated_at",
        "created_at",
        "updated_at",
    )


@admin.register(ReportExport)
class ReportExportAdmin(admin.ModelAdmin):
    list_display = (
        "report",
        "requested_by",
        "format",
        "status",
        "requested_at",
        "completed_at",
    )
    list_filter = (
        "format",
        "status",
    )
    search_fields = (
        "report__report_number",
        "requested_by__email",
        "celery_task_id",
    )
    date_hierarchy = "requested_at"
    readonly_fields = (
        "id",
        "requested_at",
        "created_at",
        "updated_at",
    )