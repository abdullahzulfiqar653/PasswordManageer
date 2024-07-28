from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/", SpectacularRedocView.as_view(url_name="schema"), name="schema-redoc"
    ),
    path("pm/api/", include("api.pm_urls")),
    path("rsa/api/", include("api.rsa_urls")),
]
