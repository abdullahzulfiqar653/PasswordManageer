from rest_framework import generics
from NeuroMail.serializers.email_rephrase import RephraseEmailCreateSerializer


class RephraseEmailCreateView(generics.CreateAPIView):
    """API to rephrase Email body"""

    serializer_class = RephraseEmailCreateSerializer
