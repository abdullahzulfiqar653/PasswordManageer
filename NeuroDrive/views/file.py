from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from NeuroDrive.serializers.file import FileSerializer
from NeuroDrive.permissions import (
    IsFileOwner,
    IsDirectoryOwner,
    IsOwnerOrSharedDirectory,
)


class FileListCreateView(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    search_fields = ["name"]
    filterset_fields = ["is_starred"]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == "POST":
            return [IsDirectoryOwner()]
        return [IsOwnerOrSharedDirectory()]

    def get_queryset(self):
        return self.request.directory.files.all().order_by("created_at")


class FileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsFileOwner]

    def perform_destroy(self, instance):
        instance.owner.remove_size(instance.size)
        return super().perform_destroy(instance)

    def get_queryset(self):
        return self.request.directory.files.all().order_by("created_at")


class FileDirecoryUpdateView(generics.UpdateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsFileOwner, IsDirectoryOwner]

    def get_queryset(self):
        return self.request.directory.files.all().order_by("created_at")

    def get_object(self):
        return self.request.file
