from rest_framework import generics
from NeuroMail.serializers.email_rephrase import RephraseEmailCreateSerializer


class RephraseEmailCreateView(generics.CreateAPIView):
    serializer_class = RephraseEmailCreateSerializer
