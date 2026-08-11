from pathlib import Path

from django.core.exceptions import ValidationError


ALLOWED_DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
}

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

ALLOWED_REPORT_EXTENSIONS = {
    ".pdf",
}

MAX_DOCUMENT_SIZE = 10 * 1024 * 1024

MAX_IMAGE_SIZE = 10 * 1024 * 1024

MAX_REPORT_SIZE = 25 * 1024 * 1024


def validate_file_extension(
    uploaded_file,
    allowed_extensions,
):
    extension = Path(
        uploaded_file.name
    ).suffix.lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            "Unsupported file extension."
        )


def validate_file_size(
    uploaded_file,
    maximum_size,
):
    if uploaded_file.size > maximum_size:
        raise ValidationError(
            "File size exceeds the permitted limit."
        )


def validate_document_file(
    uploaded_file,
):
    validate_file_extension(
        uploaded_file,
        ALLOWED_DOCUMENT_EXTENSIONS,
    )

    validate_file_size(
        uploaded_file,
        MAX_DOCUMENT_SIZE,
    )


def validate_image_file(
    uploaded_file,
):
    validate_file_extension(
        uploaded_file,
        ALLOWED_IMAGE_EXTENSIONS,
    )

    validate_file_size(
        uploaded_file,
        MAX_IMAGE_SIZE,
    )


def validate_report_file(
    uploaded_file,
):
    validate_file_extension(
        uploaded_file,
        ALLOWED_REPORT_EXTENSIONS,
    )

    validate_file_size(
        uploaded_file,
        MAX_REPORT_SIZE,
    )