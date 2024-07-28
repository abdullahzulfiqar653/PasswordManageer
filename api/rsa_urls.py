from django.urls import path
from api.views import (
    RecipientListCreateView,
    KeyPairListCreateView,
    EncryptMessageView,
    DecryptMessageView,
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
]
