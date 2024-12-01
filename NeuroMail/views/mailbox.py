from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from NeuroMail.models.mailbox import MailBox
from NeuroMail.serializers.mailbox import MailboxSerializer
from NeuroMail.utils.mail_server_apis import delete_mail_box


class MailBoxExistenceCheckView(generics.CreateAPIView):
    """This Api is for checking that if email user choosed is available or taken."""

    serializer_class = MailboxSerializer

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
            {"available": True, "message": "MailBox is available to add."},
            status=status.HTTP_200_OK,
        )


class MailBoxListCreateView(generics.ListCreateAPIView):
    """
    MailBox api to list user mailboxes or to create.
    """

    serializer_class = MailboxSerializer

    def get_queryset(self):
        return self.request.user.mailboxes.all()


class MailBoxRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    """
    MailBox APIs to delete list of mailbox or to retrieve a specific mailbox of user.
    """

    serializer_class = MailboxSerializer

    def get_queryset(self):
        return self.request.user.mailboxes.all()

    def perform_destroy(self, instance: MailBox):
        success, msg = delete_mail_box([instance.email])
        if success:
            super().perform_destroy(instance)
        else:
            raise APIException(detail=msg, code=400)
