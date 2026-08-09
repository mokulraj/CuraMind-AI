from django.contrib import admin

from .models import Address, Department, EmergencyContact, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "organization",
    )

    search_fields = (
        "name",
        "organization__name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "city",
        "state",
        "country",
    )

    list_filter = (
        "country",
        "state",
    )

    search_fields = (
        "city",
        "state",
        "country",
        "postal_code",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "relationship",
        "phone_number",
        "is_active",
        "created_at",
    )

    list_filter = (
        "relationship",
        "is_active",
    )

    search_fields = (
        "full_name",
        "phone_number",
        "alternate_phone_number",
        "email",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )