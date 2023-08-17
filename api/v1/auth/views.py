import secrets

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.utils import timezone
from djoser.serializers import TokenCreateSerializer, TokenSerializer
from djoser.utils import login_user, logout_user
from drf_spectacular.utils import extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.auth import schema
from api.v1.auth.serializers import SignupSerializer
from api.v1.serializers import DummySerializer
from sms import send_sms

User = get_user_model()


@extend_schema_view(**schema.AUTH_VIEW_SET_SCHEMA)
class AuthViewSet(viewsets.ViewSet):
    """Аутентификация."""

    pagination_class = None
    serializer_class = DummySerializer

    @action(methods=['post'], detail=False)
    def signup(self, request: Request):
        """Регистрирует пользователя, задает пароль и отправляет сообщение с паролем."""
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone'].as_e164
        user, created = User.objects.get_or_create(phone=phone_number)
        new_pass = ''.join(str(secrets.randbelow(10)) for idx in range(4))
        if send_sms(f'Ваш пароль: {new_pass}', phone_number):
            user.last_texted = timezone.now()
        user.set_password(new_pass)
        user.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(methods=['post'], detail=False)
    def login(self, request: Request):
        """Получает токен аутентификации пользователя."""
        serializer = TokenCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = login_user(request, serializer.user)
        if not serializer.user.is_staff:
            # обычному пользователю сразу меняем пароль на случайный
            serializer.user.set_password(secrets.token_hex(33))
            update_session_auth_hash(request, serializer.user)
            serializer.user.save()
        return Response(
            data=TokenSerializer(token).data,
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request: Request, *args, **kwargs):
        """Удаляет токен аутентификации пользователя."""
        logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
