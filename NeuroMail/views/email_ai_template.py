from rest_framework import generics

from NeuroMail.models.email_ai_template import EmailAiTemplate
from NeuroMail.serializers.email_ai_template import EmailAiTemplateSerializer


class EmailAiTemplateListView(generics.ListAPIView):
    queryset = EmailAiTemplate.objects.all()
    serializer_class = EmailAiTemplateSerializer
