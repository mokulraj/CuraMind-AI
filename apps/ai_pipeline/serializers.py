from rest_framework import serializers

from .models import (
    AIHumanReview,
    AIInferenceJob,
    AIModel,
    AIModelVersion,
    Prediction,
)


class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class AIModelVersionSerializer(
    serializers.ModelSerializer
):
    model_name = serializers.CharField(
        source="model.name",
        read_only=True,
    )

    class Meta:
        model = AIModelVersion
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "model_name",
        )


class AIInferenceJobSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = AIInferenceJob
        fields = "__all__"
        read_only_fields = (
            "id",
            "job_reference",
            "created_at",
            "updated_at",
        )


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class AIHumanReviewSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = AIHumanReview
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )