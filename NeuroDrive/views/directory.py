from rest_framework import generics, filters
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

from NeuroDrive.serializers.file import FileSerializer
from NeuroDrive.serializers.directory import DirectorySerializer

from NeuroDrive.models.directory import Directory
from NeuroDrive.models import SharedAccess, File


from NeuroDrive.permissions import (
    IsDirectoryOwner,
    IsOwnerOrSharedDirectory,
)


class DirectoryListCreateView(generics.ListCreateAPIView):
    serializer_class = DirectorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "files__name", "files__directory__name"]

    def get_queryset(self):
        return (
            self.request.user.directories.filter(parent=None, name="main")
            | Directory.objects.filter(shared_with=self.request.user)
        ).order_by("-created_at")


class DirectoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.request.user.directories.all() | Directory.objects.filter(
                shared_with=self.request.user
            )
        return Directory.objects.none()

    def get_object(self):
        try:
            obj = super().get_object()
        except:
            # If the directory is not found, you could raise an error or create a default directory.
            obj, _ = Directory.objects.get_or_create(
                owner=self.request.user, name="main"
            )
        return obj

    def perform_destroy(self, instance):
        if not instance.name == "main":
            instance.delete()


class DirectoryFileListCreateView(generics.ListCreateAPIView):
    search_fields = ["name"]
    filterset_fields = ["is_starred"]
    serializer_class = FileSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == "POST":
            return [IsDirectoryOwner()]
        return [IsOwnerOrSharedDirectory()]
    
    @swagger_auto_schema(
        operation_description=" If the directory ID is 'shared', shared files will be displayed."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        directory_id = self.kwargs.get("directory_id") or self.kwargs.get("pk")
        user = self.request.user
        if directory_id == "shared":

            return File.objects.filter(
                id__in=SharedAccess.objects.filter(user=user).values_list(
                    "item", flat=True
                )
            )

        return self.request.directory.files.all().order_by("-created_at")
