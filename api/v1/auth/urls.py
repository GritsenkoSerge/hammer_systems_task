from django.urls import include, path
from rest_framework import routers

from api.v1.auth.views import TokenCreateView, TokenDestroyView, UserViewSet

app_name = 'auth'

router_v1 = routers.DefaultRouter()

router_v1.register('users', UserViewSet, basename='auth')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('login/', TokenCreateView.as_view(), name='login'),
    path('logout/', TokenDestroyView.as_view(), name='logout'),
]
