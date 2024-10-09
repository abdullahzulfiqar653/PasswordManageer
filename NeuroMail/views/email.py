from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from NeuroMail.models.email import Email
from NeuroMail.serializers.email import EmailSerializer
from NeuroMail.utils.mail_server_apis import delete_mail_box


class EmailExistenceCheckView(generics.CreateAPIView):
    serializer_class = EmailSerializer

    def get_serializer_context(self):
        # Add `is_check=True` to the serializer's context
        context = super().get_serializer_context()
        context["is_check"] = True
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Since we are in "check mode", return a custom response with status 200
        return Response(
            {"available": True, "message": "Email is available to add."},
            status=status.HTTP_200_OK,
        )


class EmailListCreateView(generics.ListCreateAPIView):
    serializer_class = EmailSerializer

    def get_queryset(self):
        return self.request.user.emails.all()


class EmailRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = EmailSerializer

    def get_queryset(self):
        return self.request.user.emails.all()

    def perform_destroy(self, instance: Email):
        success, msg = delete_mail_box([instance.email])
        if success:
            super().perform_destroy(instance)
        else:
            raise APIException(detail=msg, code=400)
