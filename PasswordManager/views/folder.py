from rest_framework import generics, filters
from PasswordManager.serializers.folder import FolderSerializer


class FolderListCreateView(generics.ListCreateAPIView):
    serializer_class = FolderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        return self.request.user.folders.all().order_by("-created_at")


class FolderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FolderSerializer

    def get_queryset(self):
        return self.request.user.folders.all()
