from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from api.views import (
    UserSignUpView,
    UserSignInView,
    PasswordListCreateView,
    RandomPasswordCreateView,
    PasswordRetrieveUpdateDeleteView,
)


urlpatterns = [
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
