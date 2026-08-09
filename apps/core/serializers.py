from rest_framework import serializers

from .models import (
    Address,
    Department,
    EmergencyContact,
    Organization,
)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class DepartmentSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = Department
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "organization_name",
        )


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )