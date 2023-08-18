from drf_spectacular.utils import extend_schema
from rest_framework import status

from api.v1.profiles.serializers import ProfileSerializer
from api.v1.serializers import NotAuthenticatedSerializer, ValidationSerializer

PROFILE_VIEW_SET_SCHEMA = {
    'me': {
        extend_schema(
            methods=['get'],
            summary='Получить информацию о профиле.',
            responses={
                status.HTTP_200_OK: ProfileSerializer,
                status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            },
        ),
        extend_schema(
            methods=['patch'],
            summary='Изменить информацию о профиле.',
            responses={
                status.HTTP_200_OK: ProfileSerializer,
                status.HTTP_400_BAD_REQUEST: ValidationSerializer,
                status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            },
        ),
    },
}
