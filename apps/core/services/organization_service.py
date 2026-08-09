from django.db import transaction

from apps.core.models import (
    Department,
    Organization,
)


class OrganizationService:
    """
    Business operations for organizations and departments.
    """

    @staticmethod
    @transaction.atomic
    def create_organization(
        *,
        name,
        **extra_fields,
    ):
        if Organization.objects.filter(
            name=name
        ).exists():
            raise ValueError(
                "An organization with this name already exists."
            )

        return Organization.objects.create(
            name=name,
            **extra_fields,
        )

    @staticmethod
    @transaction.atomic
    def create_department(
        *,
        organization,
        name,
        **extra_fields,
    ):
        if Department.objects.filter(
            organization=organization,
            name=name,
        ).exists():
            raise ValueError(
                "This department already exists "
                "in the organization."
            )

        return Department.objects.create(
            organization=organization,
            name=name,
            **extra_fields,
        )