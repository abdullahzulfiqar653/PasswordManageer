from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from NeuroMail.views import EmailListCreateView
from NeuroMail.views import EmailRetrieveDeleteView

from main.views import (
    UserSignInView,
    UserSignUpView,
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
    # Email
    # =====================================================
    path("emails/", EmailListCreateView.as_view(), name="email-list-create"),
    path(
        "emails/<str:pk>/",
        EmailRetrieveDeleteView.as_view(),
        name="email-retrive-delete",
    ),
]
