from rest_framework import generics, filters
from NeuroMail.serializers.email import EmailSerializer


class EmailListCreateView(generics.ListCreateAPIView):
    serializer_class = EmailSerializer

    def get_queryset(self):
        return self.request.user.emails.all()


class EmailRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = EmailSerializer

    def get_queryset(self):
        return self.request.user.emails.all()
