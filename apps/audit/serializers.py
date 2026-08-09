from rest_framework import serializers

from .models import (
    AuditEvent,
    AuthenticationEvent,
    PatientDataAccessLog,
    SecurityEvent,
)


class AuditEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditEvent
        fields = "__all__"
        read_only_fields = tuple(
            field.name
            for field in AuditEvent._meta.fields
        )


class AuthenticationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationEvent
        fields = "__all__"
        read_only_fields = tuple(
            field.name
            for field in AuthenticationEvent._meta.fields
        )


class PatientDataAccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDataAccessLog
        fields = "__all__"
        read_only_fields = tuple(
            field.name
            for field in PatientDataAccessLog._meta.fields
        )


class SecurityEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityEvent
        fields = "__all__"
        read_only_fields = tuple(
            field.name
            for field in SecurityEvent._meta.fields
        )