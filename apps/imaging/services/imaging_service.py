import uuid

from django.db import transaction

from apps.imaging.models import (
    DICOMInstance,
    ImagingSeries,
    ImagingStudy,
)


class ImagingService:
    """
    Business operations for medical imaging.
    """

    @staticmethod
    @transaction.atomic
    def create_imaging_study(
        *,
        patient,
        modality,
        **extra_fields,
    ):
        study = ImagingStudy.objects.create(
            patient=patient,
            modality=modality,
            study_instance_uid=(
                f"2.25.{uuid.uuid4().int}"
            ),
            **extra_fields,
        )

        return study

    @staticmethod
    @transaction.atomic
    def create_series(
        *,
        study,
        series_number,
        modality,
        **extra_fields,
    ):
        return ImagingSeries.objects.create(
            study=study,
            series_number=series_number,
            modality=modality,
            series_instance_uid=(
                f"2.25.{uuid.uuid4().int}"
            ),
            **extra_fields,
        )

    @staticmethod
    @transaction.atomic
    def register_dicom_instance(
        *,
        series,
        instance_number,
        storage_key,
        **extra_fields,
    ):
        return DICOMInstance.objects.create(
            series=series,
            instance_number=instance_number,
            storage_key=storage_key,
            sop_instance_uid=(
                f"2.25.{uuid.uuid4().int}"
            ),
            **extra_fields,
        )