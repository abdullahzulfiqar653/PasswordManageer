from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from main.views.protected_media import ProtectedMediaView

from main.views import (
    UserSignInView,
    UserSignUpView,
    UserProfileRetrieveUpdateDeleteView,
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
    # =====================================================
    # Profile
    # =====================================================
    path(
        "media/profile/pictures/",
        UserProfileRetrieveUpdateDeleteView.as_view(),
        name="user-profile-retrieve-update-delete",
    ),
    path(
        "media/<str:file_type>/<str:file_name>/",
        ProtectedMediaView.as_view(),
        name="mail-protected-media",
    ),
]
