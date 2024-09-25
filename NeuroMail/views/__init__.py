from NeuroMail.views.email import EmailListCreateView, EmailRetrieveDeleteView
from NeuroMail.views.email_extension import EmailExtensionListView
from NeuroMail.views.email_ai_template import EmailAiTemplateListView
from NeuroMail.views.email_rephrase import RephraseEmailCreateView

__all__ = [
    "EmailListCreateView",
    "EmailExtensionListView",
    "EmailAiTemplateListView",
    "EmailRetrieveDeleteView",
    "RephraseEmailCreateView",
]
