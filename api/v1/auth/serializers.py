from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    """User signup serializer."""

    phone = PhoneNumberField(label=_('phone'), min_length=10, max_length=16)
    demo_message = serializers.CharField(min_length=4, max_length=4, read_only=True)
