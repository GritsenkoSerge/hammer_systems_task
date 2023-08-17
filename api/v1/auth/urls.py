from django.urls import include, path
from rest_framework import routers

from api.v1.auth.views import AuthViewSet

app_name = 'auth'

router = routers.DefaultRouter()
router.register('', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
