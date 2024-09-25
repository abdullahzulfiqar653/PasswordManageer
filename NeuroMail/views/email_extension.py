from rest_framework import generics

from NeuroMail.models.email_extension import EmailExtension
from NeuroMail.serializers.email_extension import EmailExtensionSerializer


class EmailExtensionListView(generics.ListAPIView):
    queryset = EmailExtension.objects.all()
    serializer_class = EmailExtensionSerializer

    def get_queryset(self):
        return super().get_queryset()
