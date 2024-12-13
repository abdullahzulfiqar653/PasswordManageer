from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from NeuroRsa.views import (
    EncryptMessageView,
    DecryptMessageView,
    KeyPairListCreateView,
    MainKeyPairCreateView,
    RecipientListCreateView,
    KeyPairRetrieveUpdateDeleteView,
    RecipientRetrieveUpdateDeleteView,
)

from main.views import (
    UserSignInView,
    UserSignUpView,
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
    path(
        "keypairs/main/",
        MainKeyPairCreateView.as_view(),
        name="main-keypairs-create",
    ),
    path(
        "keypairs/<str:pk>",
        KeyPairRetrieveUpdateDeleteView.as_view(),
        name="keypair-retrieve-update-delete",
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
        "recipients/encrypt-message/",
        EncryptMessageView.as_view(),
        name="recipients-encrypt-message",
    ),
    path(
        "recipients/decrypt-message/",
        DecryptMessageView.as_view(),
        name="recipients-decrypt-message",
    ),
    path(
        "recipients/<str:pk>/",
        RecipientRetrieveUpdateDeleteView.as_view(),
        name="recipient-retrieve-update-delete",
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
