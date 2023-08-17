from rest_framework import serializers


class DetailSerializer(serializers.Serializer):
    detail = serializers.CharField()


class ValidationSerializer(serializers.Serializer):
    """HTTP_400."""

    property_1 = serializers.CharField()
    property_2 = serializers.CharField()
    non_field_errors = serializers.ListField()


class NotAuthenticatedSerializer(DetailSerializer):
    """HTTP_401."""

    pass


class NotFoundSerializer(DetailSerializer):
    """HTTP_404."""

    pass


class DummySerializer(serializers.Serializer):
    """Заглушка для drf-spectacular, чтобы не ругался ViewSet без сериализаторов."""

    pass
