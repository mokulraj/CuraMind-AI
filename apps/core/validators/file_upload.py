from pathlib import Path

from django.core.exceptions import ValidationError


# ============================================================
# ALLOWED DOCUMENT FILE EXTENSIONS
# ============================================================

ALLOWED_DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
}


# ============================================================
# ALLOWED IMAGE FILE EXTENSIONS
# ============================================================

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


# ============================================================
# ALLOWED REPORT FILE EXTENSIONS
# ============================================================

ALLOWED_REPORT_EXTENSIONS = {
    ".pdf",
}


# ============================================================
# ALLOWED DICOM FILE EXTENSIONS
# ============================================================

ALLOWED_DICOM_EXTENSIONS = {
    ".dcm",
}


# ============================================================
# MAXIMUM FILE SIZES
# ============================================================

MAX_DOCUMENT_SIZE = 10 * 1024 * 1024

MAX_IMAGE_SIZE = 10 * 1024 * 1024

MAX_REPORT_SIZE = 25 * 1024 * 1024

MAX_DICOM_SIZE = 512 * 1024 * 1024


# ============================================================
# FILE EXTENSION VALIDATION
# ============================================================

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


# ============================================================
# FILE SIZE VALIDATION
# ============================================================

def validate_file_size(
    uploaded_file,
    maximum_size,
):
    if uploaded_file.size > maximum_size:
        raise ValidationError(
            "File size exceeds the permitted limit."
        )


# ============================================================
# DOCUMENT FILE VALIDATION
# ============================================================

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


# ============================================================
# IMAGE FILE VALIDATION
# ============================================================

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


# ============================================================
# REPORT FILE VALIDATION
# ============================================================

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


# ============================================================
# DICOM FILE VALIDATION
# ============================================================

def validate_dicom_file(
    uploaded_file,
):
    validate_file_extension(
        uploaded_file,
        ALLOWED_DICOM_EXTENSIONS,
    )

    validate_file_size(
        uploaded_file,
        MAX_DICOM_SIZE,
    )