from djoser import serializers as djoser_serializers
from djoser.serializers import UserCreateSerializer
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status

from api.v1.serializers import (
    NotAuthenticatedSerializer,
    ValidationSerializer,
)

TOKEN_CREATE_VIEW_SCHEMA = {
    'post': extend_schema(
        summary='Авторизовать пользователя.',
        description='При успешной авторизации возвращается токен.',
        responses={
            status.HTTP_200_OK: djoser_serializers.TokenSerializer,
        },
        examples=[
            OpenApiExample(
                'Example',
                request_only=True,
                value={'email': 'user@example.com', 'password': 'string'},
            ),
        ],
    ),
}

TOKEN_DESTROY_VIEW_SCHEMA = {
    'post': extend_schema(
        summary='Отозвать авторизацию пользователя.',
        description='При успешном отзыве авторизацию удаляется токен.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
}

USER_VIEW_SET_SCHEMA = {
    'create': extend_schema(
        summary='Зарегистрировать пользователя.',
        responses={
            status.HTTP_201_CREATED: UserCreateSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
    ),
}
