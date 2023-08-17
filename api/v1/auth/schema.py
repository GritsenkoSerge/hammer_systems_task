from djoser.serializers import TokenCreateSerializer, TokenSerializer
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status

from api.v1.auth.serializers import SignupSerializer
from api.v1.serializers import NotAuthenticatedSerializer, ValidationSerializer

AUTH_VIEW_SET_SCHEMA = {
    'signup': extend_schema(
        summary='Зарегистрировать пользователя.',
        request=SignupSerializer,
        responses={
            status.HTTP_201_CREATED: SignupSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
        examples=[
            OpenApiExample(
                'Example',
                request_only=True,
                value={'phone': '+79136745201'},
            ),
            OpenApiExample(
                'Example',
                response_only=True,
                value={'phone': '+7 913 674-52-05'},
            ),
        ],
    ),
    'login': extend_schema(
        summary='Аутентифицировать пользователя.',
        request=TokenCreateSerializer,
        responses={
            status.HTTP_200_OK: TokenSerializer,
        },
        examples=[
            OpenApiExample(
                'Example',
                request_only=True,
                value={'phone': '+79136745201', 'password': '0000'},
            ),
        ],
    ),
    'logout': extend_schema(
        summary='Отозвать токен аутентификации.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
}
