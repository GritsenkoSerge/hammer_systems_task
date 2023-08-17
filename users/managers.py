from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self._create_user(phone, password, **extra_fields)

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('Users require an phone field')
        user = self.model(phone=phone, **extra_fields)
        with transaction.atomic():
            user.set_password(password)
            user.save(using=self._db)
            profile_model = apps.get_model(app_label='users', model_name='Profile')
            profile_model.objects.create(user=user)
        return user
