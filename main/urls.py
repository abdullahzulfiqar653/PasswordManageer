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
    path("rsa/api/", include("NeuroRsa.urls")),
    path("mail/api/", include("NeuroMail.urls")),
    path("pm/api/", include("PasswordManager.urls")),
    path("drive/api/", include("NeuroDrive.urls")),
]
