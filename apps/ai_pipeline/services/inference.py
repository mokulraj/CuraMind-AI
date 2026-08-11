from dataclasses import dataclass
from typing import Any

import numpy as np
from django.core.exceptions import ValidationError

from apps.ai_pipeline.services.model_loader import (
    AIModelLoader,
)


@dataclass(frozen=True)
class PredictionResult:
    prediction: Any
    probabilities: list[float] | None
    model_version: str


class AIInferenceService:
    def __init__(
        self,
        model_path,
        model_version,
    ):
        self.model_version = (
            model_version
        )

        self.loader = AIModelLoader(
            model_path
        )

    def _validate_features(
        self,
        features,
    ):
        if features is None:
            raise ValidationError(
                "Prediction features are required."
            )

        if not isinstance(
            features,
            (list, tuple),
        ):
            raise ValidationError(
                "Prediction features must be a list or tuple."
            )

        if not features:
            raise ValidationError(
                "Prediction features cannot be empty."
            )

    def predict(
        self,
        features,
    ):
        self._validate_features(
            features
        )

        model = self.loader.load()

        input_array = np.asarray(
            features,
            dtype=float,
        )

        if input_array.ndim == 1:
            input_array = input_array.reshape(
                1,
                -1,
            )

        try:
            predictions = (
                model.predict(
                    input_array
                )
            )

        except (
            ValueError,
            TypeError,
        ) as exc:
            raise ValidationError(
                "AI model prediction failed."
            ) from exc

        probabilities = None

        if hasattr(
            model,
            "predict_proba",
        ):
            try:
                probability_array = (
                    model.predict_proba(
                        input_array
                    )
                )

                if len(
                    probability_array
                ):
                    probabilities = [
                        float(
                            value
                        )
                        for value in (
                            probability_array[
                                0
                            ]
                        )
                    ]

            except (
                ValueError,
                TypeError,
            ):
                probabilities = None

        prediction = predictions[0]

        if hasattr(
            prediction,
            "item",
        ):
            prediction = prediction.item()

        return PredictionResult(
            prediction=prediction,
            probabilities=probabilities,
            model_version=self.model_version,
        )

    def health_check(self):
        model = self.loader.load()

        return {
            "status": "healthy",
            "model_version": self.model_version,
            "model_type": (
                type(model).__name__
            ),
            "loaded": self.loader.is_loaded(),
        }