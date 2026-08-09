from rest_framework.viewsets import ModelViewSet

from .models import (
    Address,
    Department,
    EmergencyContact,
    Organization,
)

from .permissions import (
    IsOrganizationAdmin,
)

from .serializers import (
    AddressSerializer,
    DepartmentSerializer,
    EmergencyContactSerializer,
    OrganizationSerializer,
)


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all().order_by(
        "name"
    )

    serializer_class = OrganizationSerializer

    permission_classes = (
        IsOrganizationAdmin,
    )


class DepartmentViewSet(ModelViewSet):
    queryset = (
        Department.objects
        .select_related("organization")
        .all()
        .order_by("name")
    )

    serializer_class = DepartmentSerializer

    permission_classes = (
        IsOrganizationAdmin,
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        organization_id = (
            self.request.query_params.get(
                "organization"
            )
        )

        if organization_id:
            queryset = queryset.filter(
                organization_id=organization_id
            )

        return queryset


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()

    serializer_class = AddressSerializer

    permission_classes = (
        IsOrganizationAdmin,
    )


class EmergencyContactViewSet(ModelViewSet):
    queryset = EmergencyContact.objects.all()

    serializer_class = EmergencyContactSerializer

    permission_classes = (
        IsOrganizationAdmin,
    )