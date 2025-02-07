from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from main.services.s3 import S3Service
from NeuroDrive.models.file import File
from NeuroDrive.serializers.file import FileSerializer
from NeuroDrive.models.shared_access import SharedAccess
from NeuroDrive.permissions import IsFileOwner, IsDirectoryOwner
from NeuroDrive.serializers.file_access import FileAccessSerializer

from drf_yasg.utils import swagger_auto_schema


class FileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsFileOwner]

    @swagger_auto_schema(
        operation_description="*Retrieve* the file object, ensuring the user is the owner or has shared access.",
        responses={200: FileSerializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="*Update* file details. Requires *ownership* of the file.",
        request_body=FileSerializer,
        responses={200: FileSerializer()},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="*Delete* the file. Only the file *owner* can delete the file.",
        responses={204: "File deleted successfully"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.owner.profile.remove_size(instance.size)
        return super().perform_destroy(instance)

    def get_object(self):
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
            )
        ).distinct()
        return files


class FileDirectoryUpdateView(generics.UpdateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsFileOwner, IsDirectoryOwner]

    @swagger_auto_schema(
        operation_description="*Retrieve* all files in the directory, ordered by *creation date*.",
        responses={200: FileSerializer(many=True)},
    )
    def get_queryset(self):
        return self.request.directory.files.all().order_by("created_at")

    @swagger_auto_schema(
        operation_description="*Retrieve* a specific file object inside the directory.",
        responses={200: FileSerializer()},
    )
    def get_object(self):
        return self.request.file


class FileAccessView(generics.CreateAPIView):
    serializer_class = FileAccessSerializer
    permission_classes = [IsFileOwner]

    @swagger_auto_schema(
        operation_description="Grant *password-protected* access to a file. Only the *owner* can perform this action.",
        request_body=FileAccessSerializer,
        responses={201: "Access granted"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
