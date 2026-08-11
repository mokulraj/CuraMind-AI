import uuid
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename


ALLOWED_UPLOAD_DIRECTORIES = {
    "documents",
    "images",
    "reports",
    "temp",
}


def _sanitize_filename(filename):
    original_name = Path(
        filename
    ).name

    if not original_name:
        raise ValidationError(
            "A valid filename is required."
        )

    sanitized_name = get_valid_filename(
        original_name
    )

    if not sanitized_name:
        raise ValidationError(
            "The filename is invalid."
        )

    return sanitized_name


def _build_upload_path(
    directory,
    filename,
):
    if directory not in ALLOWED_UPLOAD_DIRECTORIES:
        raise ValidationError(
            "Invalid upload directory."
        )

    sanitized_name = _sanitize_filename(
        filename
    )

    extension = Path(
        sanitized_name
    ).suffix.lower()

    unique_name = (
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    return (
        f"uploads/"
        f"{directory}/"
        f"{unique_name}"
    )


def save_uploaded_file(
    uploaded_file,
    directory,
):
    if uploaded_file is None:
        raise ValidationError(
            "No file was provided."
        )

    upload_path = _build_upload_path(
        directory,
        uploaded_file.name,
    )

    saved_path = default_storage.save(
        upload_path,
        uploaded_file,
    )

    return saved_path


def delete_uploaded_file(
    file_path,
):
    if not file_path:
        return

    if default_storage.exists(
        file_path
    ):
        default_storage.delete(
            file_path
        )