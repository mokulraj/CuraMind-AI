import hashlib
from pathlib import Path

from django.core.exceptions import ValidationError


ALLOWED_MODEL_EXTENSIONS = {
    ".skops",
}

MAX_MODEL_SIZE = 1024 * 1024 * 1024


def validate_model_extension(
    model_path,
):
    extension = Path(
        model_path
    ).suffix.lower()

    if extension not in ALLOWED_MODEL_EXTENSIONS:
        raise ValidationError(
            "Unsupported AI model format."
        )


def validate_model_size(
    model_path,
):
    path = Path(
        model_path
    )

    if not path.is_file():
        raise ValidationError(
            "AI model file does not exist."
        )

    if path.stat().st_size > MAX_MODEL_SIZE:
        raise ValidationError(
            "AI model file exceeds the maximum size."
        )


def calculate_model_sha256(
    model_path,
):
    path = Path(
        model_path
    )

    if not path.is_file():
        raise ValidationError(
            "AI model file does not exist."
        )

    digest = hashlib.sha256()

    with path.open(
        "rb"
    ) as model_file:

        while chunk := model_file.read(
            1024 * 1024
        ):
            digest.update(
                chunk
            )

    return digest.hexdigest()


def validate_model_file(
    model_path,
):
    validate_model_extension(
        model_path
    )

    validate_model_size(
        model_path
    )

    return calculate_model_sha256(
        model_path
    )