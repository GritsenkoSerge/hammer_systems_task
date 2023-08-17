from typing import List

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.models import Q
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.models import TimeStampedMixin, UUIDMixin
from core.utils import generate_slug
from users.managers import UserManager


class User(TimeStampedMixin, UUIDMixin, AbstractUser):
    """Пользователь."""

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS: List[str] = []

    first_name = None
    last_name = None
    date_joined = None
    username = None
    email = None

    phone = PhoneNumberField(
        verbose_name=_('phone'),
        unique=True,
        max_length=16,
    )

    objects = UserManager()

    class Meta:
        db_table = 'referral_system"."user'
        ordering = ['phone']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self) -> str:
        return str(self.phone)

    def get_masked_phone(self) -> str:
        """Возвращает замаскированный номер телефона."""

        phone_number = ''
        index = 0
        for char in str(self.phone):
            if not char.isdigit():
                phone_number += char
                continue
            index += 1
            if index not in settings.PHONENUMBER_MASK_DIGITS:
                phone_number += char
                continue
            phone_number += settings.PHONENUMBER_MASK_SYMBOL

        return phone_number


class Profile(TimeStampedMixin):
    """Профиль пользователя."""

    first_name = models.CharField(_('first_name'), max_length=150, blank=True)
    last_name = models.CharField(_('last_name'), max_length=150, blank=True)
    email = models.EmailField(_('email'), blank=True)
    user = models.OneToOneField(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        primary_key=True,
    )
    referral_code = models.CharField(
        _('referral_code'),
        help_text=_('Unique referral code'),
        max_length=6,
        unique=True,
        db_index=True,
    )
    affiliate_code = models.CharField(
        _('affiliate_code'),
        help_text=_('Affiliate referral code'),
        max_length=6,
        blank=True,
    )

    class Meta:
        db_table = 'referral_system"."profile'
        ordering = ('-created_at',)
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self) -> str:
        full_name = f'{self.first_name} {self.last_name}'.strip()
        if full_name:
            return f'{full_name} ({str(self.user)})'
        return str(self.user)

    @transaction.atomic
    def save(self, **kwargs):
        while not self.referral_code:
            self.referral_code = generate_slug()
            if Profile.objects.filter(  # all_objects
                ~Q(pk=self.pk),
                referral_code=self.referral_code,
            ).exists():
                continue
        return super().save(**kwargs)

    def clean(self) -> None:
        if (
            self.affiliate_code
            and not Profile.objects.filter(  # all_objects
                ~Q(pk=self.pk),
                referral_code=self.affiliate_code,
            ).exists()
        ):
            raise ValidationError(
                {
                    'affiliate_code': _('Affiliate referral code does not exists.'),
                },
            )
        return super().clean()
