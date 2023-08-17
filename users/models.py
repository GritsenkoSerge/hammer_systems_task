from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedMixin, UUIDMixin
from users.managers import UserManager


class User(TimeStampedMixin, UUIDMixin, AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List[str] = []

    first_name = None
    last_name = None
    date_joined = None
    username = None

    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )

    objects = UserManager()

    class Meta:
        db_table = 'schema_name"."user'
        ordering = ['-created_at']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
