from apps.imaging.models import (
    DICOMInstance,
    ImagingSeries,
    ImagingStudy,
    RadiologyReport,
)


class ImagingRepository:
    """
    Database access for medical imaging.
    """

    @staticmethod
    def get_study_by_id(
        study_id,
    ):
        return (
            ImagingStudy.objects
            .select_related(
                "patient",
            )
            .filter(pk=study_id)
            .first()
        )

    @staticmethod
    def list_patient_studies(
        patient_id,
    ):
        return (
            ImagingStudy.objects
            .select_related(
                "patient",
            )
            .filter(
                patient_id=patient_id
            )
            .order_by("-requested_at")
        )

    @staticmethod
    def get_series(
        study_id,
    ):
        return (
            ImagingSeries.objects
            .filter(
                study_id=study_id
            )
            .order_by("series_number")
        )

    @staticmethod
    def get_instances(
        series_id,
    ):
        return (
            DICOMInstance.objects
            .filter(
                series_id=series_id
            )
            .order_by("instance_number")
        )

    @staticmethod
    def get_radiology_report(
        study_id,
    ):
        return (
            RadiologyReport.objects
            .select_related(
                "study",
                "radiologist",
            )
            .filter(
                study_id=study_id
            )
            .first()
        )