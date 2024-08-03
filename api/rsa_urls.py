from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from api.views import (
    UserSignInView,
    UserSignUpView,
    EncryptMessageView,
    DecryptMessageView,
    KeyPairListCreateView,
    RecipientListCreateView,
)

urlpatterns = [
    # =====================================================
    # KeyPair
    # =====================================================
    path(
        "keypairs/",
        KeyPairListCreateView.as_view(),
        name="keypairs-list-create",
    ),
    # =====================================================
    # Recipient
    # =====================================================
    path(
        "recipients/",
        RecipientListCreateView.as_view(),
        name="recipient-list-create",
    ),
    path(
        "recipients/encrypt-message",
        EncryptMessageView.as_view(),
        name="recipients-encrypt-message",
    ),
    path(
        "recipients/decrypt-message",
        DecryptMessageView.as_view(),
        name="recipients-decrypt-message",
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