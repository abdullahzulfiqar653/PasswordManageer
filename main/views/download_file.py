import requests
from rest_framework import generics
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.serializers.download_file import FileDownloadSerializer


class FileDownloadAPIView(generics.CreateAPIView):
    serializer_class = FileDownloadSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data["url"]
            try:
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
