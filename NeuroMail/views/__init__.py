from NeuroMail.views.email import (
    EmailListCreateView,
    EmailRetrieveDeleteView,
    EmailExistenceCheckView,
)
from NeuroMail.views.mailbox import (
    MailboxEmailListCreateView,
    MailboxEmailRetrieveView,
    MailboxEmailTrashView,
)
from NeuroMail.views.email_extension import EmailExtensionListView
from NeuroMail.views.email_ai_template import EmailAiTemplateListView
from NeuroMail.views.email_rephrase import RephraseEmailCreateView

__all__ = [
    "EmailListCreateView",
    "EmailExtensionListView",
    "EmailExistenceCheckView",
    "EmailAiTemplateListView",
    "EmailRetrieveDeleteView",
    "RephraseEmailCreateView",
    "MailboxEmailListCreateView",
    "MailboxEmailRetrieveView",
    "MailboxEmailTrashView",
]
