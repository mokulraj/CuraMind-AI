from pathlib import Path

from django.core.exceptions import ValidationError
from pydicom import dcmread
from pydicom.errors import InvalidDicomError


DICOM_EXTENSION = ".dcm"

MAX_DICOM_SIZE = 512 * 1024 * 1024


def validate_dicom_extension(
    uploaded_file,
):
    extension = Path(
        uploaded_file.name
    ).suffix.lower()

    if extension != DICOM_EXTENSION:
        raise ValidationError(
            "Only .dcm files are accepted for DICOM uploads."
        )


def validate_dicom_size(
    uploaded_file,
):
    if uploaded_file.size > MAX_DICOM_SIZE:
        raise ValidationError(
            "DICOM file exceeds the maximum allowed size."
        )


def validate_dicom_file(
    uploaded_file,
):
    if uploaded_file is None:
        raise ValidationError(
            "No DICOM file was provided."
        )

    validate_dicom_extension(
        uploaded_file
    )

    validate_dicom_size(
        uploaded_file
    )

    current_position = uploaded_file.tell()

    try:
        dataset = dcmread(
            uploaded_file,
            stop_before_pixels=True,
            force=False,
        )

    except (
        InvalidDicomError,
        ValueError,
        OSError,
    ) as exc:
        raise ValidationError(
            "The uploaded file is not a valid DICOM file."
        ) from exc

    finally:
        uploaded_file.seek(
            current_position
        )

    if not getattr(
        dataset,
        "SOPClassUID",
        None,
    ):
        raise ValidationError(
            "DICOM SOP Class UID is missing."
        )

    return dataset