from django.conf import settings
from django.contrib import admin
from django.urls import path, include, URLPattern, URLResolver
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)


urlpatterns: list[URLPattern | URLResolver] = [
    path('api/wallets/', include('wallets.urls')),
    path('admin/', admin.site.urls),
]


# Swagger UI & Debug Toolbar
if settings.DEBUG:
    urlpatterns += [
        path(
            'api/schema/',
            SpectacularAPIView.as_view(),
            name='schema'),
        path(
            'swagger/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger-ui'),
        path(
            'redoc/',
            SpectacularRedocView.as_view(url_name='schema'),
            name='redoc'),

        path('__debug__/', include('debug_toolbar.urls')),
    ]
