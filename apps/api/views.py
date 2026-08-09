from django.conf import settings

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    Lightweight application health endpoint.

    This endpoint does not require authentication.
    """

    permission_classes = (
        AllowAny,
    )

    authentication_classes = ()

    @extend_schema(
        responses=inline_serializer(
            name="HealthCheckResponse",
            fields={
                "status": serializers.CharField(),
                "service": serializers.CharField(),
                "environment": serializers.CharField(),
            },
        )
    )
    def get(self, request):
        return Response(
            {
                "status": "ok",
                "service": "CuraMind AI",
                "environment": getattr(
                    settings,
                    "ENVIRONMENT",
                    "unknown",
                ),
            },
            status=status.HTTP_200_OK,
        )