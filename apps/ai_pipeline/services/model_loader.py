from pathlib import Path
from threading import Lock

import skops.io as sio
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.ai_pipeline.validators.model import (
    calculate_model_sha256,
    validate_model_file,
)


class AIModelLoader:
    def __init__(
        self,
        model_path,
    ):
        self.model_path = Path(
            model_path
        )

        self._model = None

        self._lock = Lock()

    def _resolve_model_path(self):
        if not self.model_path.is_absolute():
            return (
                settings.BASE_DIR
                / self.model_path
            )

        return self.model_path

    def _validate_model(self):
        resolved_path = (
            self._resolve_model_path()
        )

        expected_hash = (
            getattr(
                settings,
                "AI_MODEL_SHA256",
                "",
            )
        )

        actual_hash = (
            validate_model_file(
                resolved_path
            )
        )

        if expected_hash:
            if actual_hash.lower() != (
                expected_hash.lower()
            ):
                raise ValidationError(
                    "AI model checksum verification failed."
                )

        return resolved_path

    def load(self):
        if self._model is not None:
            return self._model

        with self._lock:
            if self._model is not None:
                return self._model

            model_path = (
                self._validate_model()
            )

            unknown_types = (
                sio.get_untrusted_types(
                    file=str(
                        model_path
                    )
                )
            )

            trusted_types = getattr(
                settings,
                "AI_MODEL_TRUSTED_TYPES",
                [],
            )

            unknown_type_names = {
                str(item)
                for item in unknown_types
            }

            trusted_type_names = {
                str(item)
                for item in trusted_types
            }

            if not unknown_type_names.issubset(
                trusted_type_names
            ):
                raise ValidationError(
                    "AI model contains untrusted types."
                )

            self._model = sio.load(
                str(
                    model_path
                ),
                trusted=list(
                    trusted_type_names
                ),
            )

            return self._model

    def checksum(self):
        model_path = (
            self._resolve_model_path()
        )

        return calculate_model_sha256(
            model_path
        )

    def is_loaded(self):
        return self._model is not None