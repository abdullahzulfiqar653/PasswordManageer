from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from main.views.protected_media import ProtectedMediaView

from PasswordManager.views import (
    FolderListCreateView,
    PasswordListCreateView,
    BulkPasswordDeleteView,
    RandomPasswordCreateView,
    FolderRetrieveUpdateDeleteView,
    PasswordRetrieveUpdateDeleteView,
)

from main.views import (
    UserSignInView,
    UserSignUpView,
    RefreshTokenAPIView,
)

urlpatterns = [
    # =====================================================
    # Folders
    # =====================================================
    path(
        "folders/",
        FolderListCreateView.as_view(),
        name="folde-list-create",
    ),
    path(
        "folders/<str:pk>/",
        FolderRetrieveUpdateDeleteView.as_view(),
        name="folder-detail",
    ),
    # =====================================================
    # Password
    # =====================================================
    path(
        "passwords/",
        PasswordListCreateView.as_view(),
        name="password-list-create",
    ),
    path(
        "passwords/generate-random/",
        RandomPasswordCreateView.as_view(),
        name="generate-random",
    ),
    path(
        "passwords/delete/",
        BulkPasswordDeleteView.as_view(),
        name="bulk-password-delete",
    ),
    path(
        "passwords/<str:pk>/",
        PasswordRetrieveUpdateDeleteView.as_view(),
        name="password-detail",
    ),
    # =====================================================
    # User
    # =====================================================
    path("user/token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("user/generate-token/", UserSignInView.as_view(), name="generate-token"),
    path(
        "user/generate-pass-phrase/",
        UserSignUpView.as_view(),
        name="generate-pass-phrase",
    ),
    path("user/refresh-token/", RefreshTokenAPIView.as_view(), name="refresh-token"),
    path(
        "media/<str:file_type>/<str:file_name>/",
        ProtectedMediaView.as_view(),
        name="password-protected-media",
    ),
]
