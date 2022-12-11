from rest_framework import serializers
from apps.endpoints.models import Endpoint, MLAlgorithm, MLRequest


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "created_at")
        fields = read_only_fields


class MLAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithm
        read_only_fields = (
            "id",
            "name",
            "description",
            "code",
            "version",
            "creator",
            "created_at",
            "parent_endpoint",
        )
        fields = read_only_fields


class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = (
            "id",
            "input_data",
            "response",
            "created_at",
            "parent_mlalgorithm",
        )
        fields = read_only_fields
