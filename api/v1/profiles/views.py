from django.contrib.auth import get_user_model
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import OuterRef
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.v1.profiles import schema
from api.v1.profiles.serializers import ProfileSerializer
from users.models import Profile

User = get_user_model()


@extend_schema_view(**schema.PROFILE_VIEW_SET_SCHEMA)
class ProfileViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        referrals_subquery = Profile.objects.filter(
            affiliate_code=OuterRef('referral_code'),
        ).values('user__phone')
        return Profile.objects.annotate(referrals=ArraySubquery(referrals_subquery))

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def get_instance(self):
        return get_object_or_404(self.get_queryset(), user=self.request.user)

    @action(methods=['get', 'patch'], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
