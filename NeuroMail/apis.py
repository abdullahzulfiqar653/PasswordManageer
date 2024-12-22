from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from main.views.protected_media import ProtectedMediaView


from NeuroMail.views import (
    MailBoxListCreateView,
    EmailExtensionListView,
    EmailAiTemplateListView,
    RephraseEmailCreateView,
    MailBoxRetrieveDeleteView,
    MailBoxExistenceCheckView,
    MailboxEmailListCreateView,
    MailboxEmailMoveToTrashView,
    MailboxEmailRetrieveUpdateView,
    MailboxEmailRestoreFromTrashView,
)

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
    path(
        "user/profile/",
        UserProfileRetrieveUpdateDeleteView.as_view(),
        name="user-profile-retrieve-update-delete",
    ),
    # =====================================================
    # MailBox
    # =====================================================
    path("mailbox/", MailBoxListCreateView.as_view(), name="mailbox-list-create"),
    path(
        "mailbox/extensions/",
        EmailExtensionListView.as_view(),
        name="mailbox-extension-list",
    ),
    path(
        "mailbox/existance/verify/",
        MailBoxExistenceCheckView.as_view(),
        name="mailbox-existance-verify",
    ),
    path(
        "mailbox/<str:pk>/",
        MailBoxRetrieveDeleteView.as_view(),
        name="mailbox-retrive-delete",
    ),
    # =====================================================
    # Email
    # =====================================================
    path(
        "mailbox/<str:mailbox_id>/emails/",
        MailboxEmailListCreateView.as_view(),
        name="mailbox-email-list-create",
    ),
    path(
        "mailbox/<str:mailbox_id>/emails/move-to-trash/",
        MailboxEmailMoveToTrashView.as_view(),
        name="mailbox-email-move-to-trash",
    ),
    path(
        "mailbox/<str:mailbox_id>/emails/restore-from-trash/",
        MailboxEmailRestoreFromTrashView.as_view(),
        name="mailbox-email-restore-from-trash",
    ),
    path(
        "mailbox/<str:mailbox_id>/emails/<str:pk>/",
        MailboxEmailRetrieveUpdateView.as_view(),
        name="mailbox-email-retrieve-update",
    ),
    path(
        "emails/ai/templates/",
        EmailAiTemplateListView.as_view(),
        name="email-ai-templates-list",
    ),
    path(
        "emails/ai/rephrase/",
        RephraseEmailCreateView.as_view(),
        name="rephrase-email-create",
    ),
    # =====================================================
    # Profile
    # =====================================================
    path(
        "media/<str:file_type>/<str:file_name>/",
        ProtectedMediaView.as_view(),
        name="mail-protected-media",
    ),
]
