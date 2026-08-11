from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from pydicom import dcmread
from pydicom.errors import InvalidDicomError


SAFE_METADATA_FIELDS = (
    "Modality",
    "StudyInstanceUID",
    "SeriesInstanceUID",
    "SOPInstanceUID",
    "SOPClassUID",
    "StudyDate",
    "StudyTime",
    "SeriesNumber",
    "InstanceNumber",
    "Rows",
    "Columns",
    "NumberOfFrames",
    "SamplesPerPixel",
    "PhotometricInterpretation",
    "BitsAllocated",
    "BitsStored",
    "HighBit",
    "PixelRepresentation",
    "TransferSyntaxUID",
)


def read_dicom_metadata(
    file_path,
):
    if not file_path:
        raise ValidationError(
            "DICOM file path is required."
        )

    if not default_storage.exists(
        file_path
    ):
        raise ValidationError(
            "DICOM file does not exist."
        )

    absolute_path = Path(
        default_storage.path(
            file_path
        )
    )

    try:
        dataset = dcmread(
            absolute_path,
            stop_before_pixels=True,
            force=False,
        )

    except (
        InvalidDicomError,
        OSError,
        ValueError,
    ) as exc:
        raise ValidationError(
            "Unable to read the DICOM file."
        ) from exc

    metadata = {}

    for field in SAFE_METADATA_FIELDS:
        if hasattr(
            dataset,
            field,
        ):
            value = getattr(
                dataset,
                field,
            )

            if value is not None:
                metadata[field] = str(
                    value
                )

    if (
        "TransferSyntaxUID"
        not in metadata
        and hasattr(
            dataset,
            "file_meta",
        )
        and getattr(
            dataset.file_meta,
            "TransferSyntaxUID",
            None,
        )
    ):
        metadata[
            "TransferSyntaxUID"
        ] = str(
            dataset.file_meta.TransferSyntaxUID
        )

    return metadata


def get_dicom_dataset(
    file_path,
):
    if not file_path:
        raise ValidationError(
            "DICOM file path is required."
        )

    if not default_storage.exists(
        file_path
    ):
        raise ValidationError(
            "DICOM file does not exist."
        )

    absolute_path = Path(
        default_storage.path(
            file_path
        )
    )

    try:
        return dcmread(
            absolute_path,
            force=False,
        )

    except (
        InvalidDicomError,
        OSError,
        ValueError,
    ) as exc:
        raise ValidationError(
            "Unable to read the DICOM file."
        ) from exc


def get_pixel_array(
    file_path,
):
    dataset = get_dicom_dataset(
        file_path
    )

    try:
        return dataset.pixel_array

    except (
        AttributeError,
        ValueError,
        RuntimeError,
        NotImplementedError,
    ) as exc:
        raise ValidationError(
            "Unable to decode DICOM pixel data."
        ) from exc


def get_transfer_syntax(
    file_path,
):
    dataset = get_dicom_dataset(
        file_path
    )

    transfer_syntax = getattr(
        dataset.file_meta,
        "TransferSyntaxUID",
        None,
    )

    if transfer_syntax is None:
        raise ValidationError(
            "DICOM transfer syntax is missing."
        )

    return str(
        transfer_syntax
    )


def get_image_dimensions(
    file_path,
):
    dataset = get_dicom_dataset(
        file_path
    )

    rows = getattr(
        dataset,
        "Rows",
        None,
    )

    columns = getattr(
        dataset,
        "Columns",
        None,
    )

    if rows is None or columns is None:
        raise ValidationError(
            "DICOM image dimensions are missing."
        )

    return {
        "rows": int(rows),
        "columns": int(columns),
    }