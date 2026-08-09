from apps.core.models import (
    Department,
    Organization,
)


class OrganizationRepository:
    """
    Database access for organizations and departments.
    """

    @staticmethod
    def get_organization_by_id(
        organization_id,
    ):
        return (
            Organization.objects
            .filter(pk=organization_id)
            .first()
        )

    @staticmethod
    def list_organizations():
        return (
            Organization.objects
            .all()
            .order_by("name")
        )

    @staticmethod
    def get_department_by_id(
        department_id,
    ):
        return (
            Department.objects
            .select_related("organization")
            .filter(pk=department_id)
            .first()
        )

    @staticmethod
    def list_departments(
        organization_id=None,
    ):
        queryset = (
            Department.objects
            .select_related("organization")
        )

        if organization_id:
            queryset = queryset.filter(
                organization_id=organization_id
            )

        return queryset.order_by("name")