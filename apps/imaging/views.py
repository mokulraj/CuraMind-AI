from rest_framework.viewsets import ModelViewSet

from .models import (
    DICOMInstance,
    ImagingAIProcessing,
    ImagingSeries,
    ImagingStudy,
    RadiologyReport,
)

from .permissions import (
    CanAccessImaging,
    CanManageImaging,
)

from .serializers import (
    DICOMInstanceSerializer,
    ImagingAIProcessingSerializer,
    ImagingSeriesSerializer,
    ImagingStudySerializer,
    RadiologyReportSerializer,
)


class ImagingStudyViewSet(ModelViewSet):
    serializer_class = ImagingStudySerializer

    def get_queryset(self):
        user = self.request.user

        queryset = (
            ImagingStudy.objects
            .select_related("patient")
            .all()
            .order_by("-created_at")
        )

        if not user.is_authenticated:
            return queryset.none()

        if user.is_superuser:
            return queryset

        role = getattr(
            user,
            "role",
            None,
        )

        if role == "PATIENT":
            patient = getattr(
                user,
                "patient_profile",
                None,
            )

            if patient:
                return queryset.filter(
                    patient=patient
                )

            return queryset.none()

        if role in {
            "DOCTOR",
            "RADIOLOGIST",
            "NURSE",
            "STAFF",
            "ADMIN",
        }:
            return queryset

        return queryset.none()

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                CanManageImaging()
            ]

        return [
            CanAccessImaging()
        ]


class ImagingSeriesViewSet(ModelViewSet):
    queryset = (
        ImagingSeries.objects
        .select_related("study")
        .all()
        .order_by("series_number")
    )

    serializer_class = ImagingSeriesSerializer

    permission_classes = (
        CanAccessImaging,
    )


class DICOMInstanceViewSet(ModelViewSet):
    queryset = (
        DICOMInstance.objects
        .select_related("series")
        .all()
        .order_by("instance_number")
    )

    serializer_class = DICOMInstanceSerializer

    permission_classes = (
        CanManageImaging,
    )


class RadiologyReportViewSet(ModelViewSet):
    queryset = (
        RadiologyReport.objects
        .select_related(
            "study",
            "radiologist",
        )
        .all()
        .order_by("-created_at")
    )

    serializer_class = RadiologyReportSerializer

    permission_classes = (
        CanAccessImaging,
    )


class ImagingAIProcessingViewSet(ModelViewSet):
    queryset = ImagingAIProcessing.objects.all()

    serializer_class = ImagingAIProcessingSerializer

    permission_classes = (
        CanManageImaging,
    )