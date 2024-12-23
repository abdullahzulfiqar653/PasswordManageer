from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from main.views.protected_media import ProtectedMediaView

from main.views import (
    UserSignInView,
    UserSignUpView,
    UserProfileRetrieveUpdateView,
)

from NeuroDrive.views import (
    FileListCreateView,
    DirectoryListCreateView,
    FileRetrieveUpdateDestroyView,
    DirectoryRetrieveUpdateDestroyView,
)

urlpatterns = [
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
    path(
        "user/profile/",
        UserProfileRetrieveUpdateView.as_view(),
        name="user-profile-retrieve-update-delete",
    ),
    # =====================================================
    # Media
    # =====================================================
    path(
        "media/<str:file_type>/<str:file_name>/",
        ProtectedMediaView.as_view(),
        name="mail-protected-media",
    ),
    # =====================================================
    # Directories
    # =====================================================
    path(
        "directories/", DirectoryListCreateView.as_view(), name="directory-list-create"
    ),
    path(
        "directories/<str:pk>/",
        DirectoryRetrieveUpdateDestroyView.as_view(),
        name="directory-retrieve-update-destroy",
    ),
    path(
        "directories/<str:directory_id>/files/",
        FileListCreateView.as_view(),
        name="file-list-create",
    ),
    # =====================================================
    # Files
    # =====================================================
    path(
        "files/<str:pk>/",
        FileRetrieveUpdateDestroyView.as_view(),
        name="file-retrieve-update-destroy",
    ),
]
