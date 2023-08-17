from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

app_name = 'api'

urls_v1 = [
    path('auth/', include('api.v1.auth.urls', namespace='auth')),
]


urlpatterns = [
    path('v1/', include(urls_v1)),
    path('v1/schema/', SpectacularAPIView.as_view(), name='openapi-schema'),
    path(
        'v1/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='api:openapi-schema'),
        name='swagger-ui',
    ),
    path(
        'v1/schema/redoc/',
        SpectacularRedocView.as_view(url_name='api:openapi-schema'),
        name='redoc',
    ),
]
