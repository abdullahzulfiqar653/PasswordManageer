from rest_framework import generics
from rest_framework.exceptions import APIException

from NeuroMail.models.email import Email
from NeuroMail.serializers.email import EmailSerializer
from NeuroMail.utils.mail_server_apis import delete_mail_box


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
