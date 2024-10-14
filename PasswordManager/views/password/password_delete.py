from rest_framework import generics, status
from rest_framework.response import Response

from PasswordManager.serializers.password_delete import PasswordDeleteSerializer


class BulkPasswordDeleteView(generics.CreateAPIView):
    serializer_class = PasswordDeleteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.delete_passwords()
            return Response(
                {"message": "Passwords deleted successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
