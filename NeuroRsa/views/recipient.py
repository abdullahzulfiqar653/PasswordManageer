from rest_framework import generics, filters
from NeuroRsa.serializers.recipient import RecipientSerializer


class RecipientListCreateView(generics.ListCreateAPIView):
    serializer_class = RecipientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        return self.request.user.recipients.all().order_by("-created_at")


class RecipientRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipientSerializer

    def get_queryset(self):
        return self.request.user.recipients.all()
