from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Schema generation endpoint
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    # Interactive documentation endpoints
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Versioned API endpoints
    path('', include('accounts.api_urls')),
    path('', include('chat.api_urls')),
]