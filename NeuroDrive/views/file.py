from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.hashers import check_password
from main.services.s3 import S3Service
from NeuroDrive.models.file import File
from NeuroDrive.models.shared_access import SharedAccess
from NeuroDrive.serializers.file import FileSerializer 
from NeuroDrive.permissions import (
    IsFileOwner,
    IsDirectoryOwner
)

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

        # Verify if the user is the owner
        if obj.owner != self.request.user:
            # Check if the user has shared access to the file with READ or FULL permission
            shared_access = SharedAccess.objects.filter(
                user=self.request.user,
                item=obj,
                permission_type__in=[
                    SharedAccess.Permission.READ,
                    SharedAccess.Permission.FULL,
                ],
            )

            if not shared_access.exists():
                raise PermissionDenied(
                    "You do not have permission to access this file."
                )
            
        if obj.password:   
            entered_password = self.request.query_params.get('password')

            if not entered_password:
                raise PermissionDenied("Password required to access this file.")

            if not check_password(entered_password, obj.password):
                raise PermissionDenied("Incorrect password.")

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
