from django.urls import include, path
from rest_framework import routers

from api.v1.profiles.views import ProfileViewSet

app_name = 'profiles'

router = routers.DefaultRouter()
router.register('', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
]
