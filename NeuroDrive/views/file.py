from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from main.services.s3 import S3Service

from NeuroDrive.models.file import File
from NeuroDrive.serializers.file import FileSerializer
from NeuroDrive.models.shared_access import SharedAccess
from NeuroDrive.permissions import IsFileOwner, IsDirectoryOwner
from NeuroDrive.serializers.fileAccess import FileAccessSerializer


class FileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsFileOwner]

    def perform_destroy(self, instance):
        instance.owner.profile.remove_size(instance.size)
        return super().perform_destroy(instance)

    def get_object(self):
        """
        Retrieve the file object, and check if the user is either the owner or has access through SharedAccess.
        """
        # Retrieve the file object based on the primary key

        obj = super().get_object()
        
        if self.request.method == "DELETE":
          return obj

        if obj.password :
            raise PermissionDenied(
                "File is Password Protected. You cannot access this file."
            )

        s3_client = S3Service()
        obj.url = s3_client.generate_presigned_url(obj.s3_url)
        return obj

    def get_queryset(self):
        """
        Return all files that the user owns or has access to through SharedAccess.
        """
        user = self.request.user

        # Using Q objects to combine both conditions in a single queryset
        files = File.objects.filter(
            Q(owner=user)  # User owns the file
            | Q(
                shared_accesses__user=user,
                shared_accesses__permission_type__in=[
                    SharedAccess.Permission.READ,
                    SharedAccess.Permission.WRITE,
                    SharedAccess.Permission.FULL,
                ],
            )  # User has shared access to the file
        ).distinct()  # Ensure distinct results
        return files


class FileDirecoryUpdateView(generics.UpdateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsFileOwner, IsDirectoryOwner]

    def get_queryset(self):
        return self.request.directory.files.all().order_by("created_at")

    def get_object(self):
        return self.request.file


class FileAccessView(generics.CreateAPIView):
    serializer_class = FileAccessSerializer
    permission_classes = [IsFileOwner]
