from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import DoctorProfile, PatientProfile, StaffProfile, User


@admin.register(User)
class CuraMindUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = (
        "email",
        "full_name",
        "role",
        "is_active",
        "is_staff",
        "created_at",
    )
    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "last_login",
    )

    fieldsets = (
        (
            "Authentication",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Authorization",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Security",
            {
                "fields": (
                    "last_login",
                )
            },
        ),
        (
            "System",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )