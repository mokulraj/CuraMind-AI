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
        read_only_fields = "__all__"


class AuthenticationEventSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = AuthenticationEvent
        fields = "__all__"
        read_only_fields = "__all__"


class PatientDataAccessLogSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = PatientDataAccessLog
        fields = "__all__"
        read_only_fields = "__all__"


class SecurityEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityEvent
        fields = "__all__"
        read_only_fields = "__all__"