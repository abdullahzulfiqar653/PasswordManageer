from rest_framework import generics, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser

from NeuroDrive.models import SharedAccess, File
from NeuroDrive.models.directory import Directory
from NeuroDrive.serializers.file import FileSerializer
from NeuroDrive.serializers.directory import DirectorySerializer

from NeuroDrive.permissions import (
    IsDirectoryOwner,
    IsOwnerOrSharedDirectory,
)
from drf_yasg.utils import swagger_auto_schema



class DirectoryListCreateView(generics.ListCreateAPIView):
    """
    **API Endpoint: Directory List & Create**
    - **GET**: Retrieves a list of directories owned or shared with the user.
    - **POST**: Creates a new directory.
    """

    serializer_class = DirectorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "files__name", "files__directory__name"]

    @swagger_auto_schema(
        operation_description="**This endpoint is used to retrieve directories that:**\n\n"
        "- Are owned by the authenticated user\n"
        "- Are shared with the authenticated user",
        responses={200: DirectorySerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="**This endpoint is used to create a new directory with the following data:**\n\n"
        "- `name`: Name of the directory\n"
        "- `parent`: (Optional) Parent directory ID\n",
        request_body=DirectorySerializer,
        responses={201: DirectorySerializer()},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return (
            self.request.user.directories.filter(parent=None, name="main")
            | Directory.objects.filter(shared_with=self.request.user)
        ).order_by("-created_at")


class DirectoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    - **PATCH**: Update directory details.
  
    """

    serializer_class = DirectorySerializer

    @swagger_auto_schema(
        operation_description="This endpoint is used to *retrieve* the details of a specific directory by ID.",
        responses={200: DirectorySerializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="**This endpoint is used to *update* directory details with the following fields:**\n\n"
        "- `name`: (Optional) New name of the directory\n"
        "- `parent`: (Optional) Update parent directory ID\n",
        request_body=DirectorySerializer,
        responses={200: DirectorySerializer()},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="**This endpoint is used to *delete* a directory (except the main directory).**",
        responses={204: "Directory deleted successfully"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

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
    """
    **API Endpoint: Directory Files List & Create**
    - **GET**: Retrieve files in a directory.
    - **POST**: Upload a new file to the directory.
    """

    search_fields = ["name"]
    filterset_fields = ["is_starred"]
    serializer_class = FileSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    parser_classes = (MultiPartParser, FormParser)  # Allow file uploads

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == "POST":
            return [IsDirectoryOwner()]
        return [IsOwnerOrSharedDirectory()]

    @swagger_auto_schema(
        operation_description="**This endpoint is used to *retrieve* files in a directory.**\n\n"
        "- If the directory ID is `shared`, shared files will be displayed.",
        responses={200: FileSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="**This endpoint is used to *upload* a new file to a directory with the following fields:**\n\n"

        "- `directory`: Directory ID where file is being uploaded\n"
        "- `file`: The actual file to upload (supports images, PDFs, etc.)",
        request_body=FileSerializer,
        responses={201: FileSerializer()},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    def perform_create(self, serializer):
        """
        Handle file upload to the directory.
        """
        directory_id = self.kwargs.get("directory_id")
        if not directory_id:
            raise PermissionDenied("Directory ID is required for file upload.")
        try:
            directory = Directory.objects.get(id=directory_id)
        except Directory.DoesNotExist:
            raise PermissionDenied("The specified directory does not exist.")

        serializer.save(directory=directory)
