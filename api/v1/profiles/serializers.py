from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.models import Profile

User = get_user_model()


class PhoneListField(serializers.ListField):
    """Сериализатор списка телефонов."""

    phone = PhoneNumberField(label=_('phone'), min_length=10, max_length=16)


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя."""

    referrals = PhoneListField()  # (read_only=True, many=True)

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'email',
            'referral_code',
            'affiliate_code',
            'referrals',
        )
        read_only_fields = ('referral_code',)

    def validate(self, attrs):
        if (
            not attrs
            or not (affiliate_code := attrs.get('affiliate_code'))
            or Profile.objects.filter(referral_code=affiliate_code).exists()
        ):
            return attrs
        raise serializers.ValidationError(
            {
                'affiliate_code': _('Affiliate referral code does not exists.'),
            },
        )
