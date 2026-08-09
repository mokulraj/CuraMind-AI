from django.contrib import admin

from .models import (
    Appointment,
    AppointmentNote,
    DoctorAvailability,
)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "doctor",
        "status",
        "appointment_type",
        "consultation_mode",
        "scheduled_start",
        "scheduled_end",
    )
    list_filter = (
        "status",
        "appointment_type",
        "consultation_mode",
    )
    search_fields = (
        "patient__user__email",
        "doctor__user__email",
    )
    date_hierarchy = "scheduled_start"
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "weekday",
        "start_time",
        "end_time",
        "is_active",
    )
    list_filter = (
        "weekday",
        "is_active",
    )
    search_fields = (
        "doctor__user__email",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(AppointmentNote)
class AppointmentNoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "appointment",
        "author",
        "created_at",
    )
    search_fields = (
        "appointment__patient__user__email",
        "author__email",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )