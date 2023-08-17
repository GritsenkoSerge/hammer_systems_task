from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins, viewsets

from api.v1.auth import schema
from api.v1.serializers import DummySerializer

User = get_user_model()


@extend_schema_view(**schema.TOKEN_CREATE_VIEW_SCHEMA)
class TokenCreateView(DjoserTokenCreateView):
    pass


@extend_schema_view(**schema.TOKEN_DESTROY_VIEW_SCHEMA)
class TokenDestroyView(DjoserTokenDestroyView):
    serializer_class = DummySerializer


@extend_schema_view(**schema.USER_VIEW_SET_SCHEMA)
class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    class Meta:
        model = User
