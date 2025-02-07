from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.serializers.download_file import FileDownloadSerializer
import requests

class FileDownloadAPIView(generics.CreateAPIView):
    serializer_class = FileDownloadSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="This endpoint allows the authenticated user to download a file by providing a valid URL.",
        request_body=FileDownloadSerializer,
        responses={
            200: "File successfully downloaded.",
            400: "Invalid request or failed to download the file.",
            401: "Unauthorized access.",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        **POST Parameters**:
        - `url`: The URL of the file to download.

        **Behavior**:
        - The user must be authenticated to use this endpoint.
        - The file will be downloaded by the provided URL and sent as an attachment for the user to download.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data["url"]
            try:
                # Send the request to get the file
                response = requests.get(url, stream=True)
                response.raise_for_status()  # Ensure we notice bad responses
                content_type = response.headers.get(
                    "Content-Type", "application/octet-stream"
                )

                # Create a response object and set the content type and disposition
                file_response = HttpResponse(
                    response.content, content_type=content_type
                )
                file_response["Content-Disposition"] = (
                    'attachment; filename="downloaded_file"'
                )

                return file_response
            except requests.exceptions.RequestException as e:
                return Response(
                    {"error": str(e)}, status=response.status_code if response else 400
                )
        return Response(serializer.errors, status=400)
