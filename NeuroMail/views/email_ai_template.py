from rest_framework import generics

from NeuroMail.models.email_ai_template import EmailAiTemplate
from NeuroMail.serializers.email_ai_template import EmailAiTemplateSerializer


class EmailAiTemplateListView(generics.ListAPIView):
    """This api provide templates[Donald trump, michal obama] that will be used in new email box to rephrase emails"""

    queryset = EmailAiTemplate.objects.all()
    serializer_class = EmailAiTemplateSerializer
