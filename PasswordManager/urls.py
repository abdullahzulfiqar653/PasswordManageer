from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from PasswordManager.views import (
    PasswordListCreateView,
    BulkPasswordDeleteView,
    RandomPasswordCreateView,
    PasswordRetrieveUpdateDeleteView,
    FolderListCreateView,
    FolderRetrieveUpdateDeleteView,
)

from main.views import (
    UserSignInView,
    UserSignUpView,
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
]
