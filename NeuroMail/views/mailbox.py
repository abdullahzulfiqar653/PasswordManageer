from rest_framework.response import Response
from rest_framework import generics, exceptions, status
from django_filters.rest_framework import DjangoFilterBackend

from NeuroMail.models.email import Email
from NeuroMail.serializers.mailbox import MailBoxSerializer
from NeuroMail.serializers.mailbox_trash import MailboxTrashSerializer


class MailboxEmailListCreateView(generics.ListCreateAPIView):
    serializer_class = MailBoxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["email_type", "is_starred"]

    def get_queryset(self):
        selected_email = self.request.query_params.get("email")
        if not selected_email:
            raise exceptions.ValidationError(
                {"error": "No email provided in the query parameters."}
            )
        # Get the email object associated with the user
        try:
            email_account = self.request.user.emails.get(email=selected_email)
            return email_account.email_boxes.all()
        except Email.DoesNotExist:
            raise exceptions.PermissionDenied({"error": "Invalid email selected."})


class MailboxEmailRetrieveView(generics.RetrieveAPIView):
    serializer_class = MailBoxSerializer

    def get_queryset(self):
        selected_email = self.request.query_params.get("email")
        if not selected_email:
            raise exceptions.ValidationError(
                {"error": "No email provided in the query parameters."}
            )

        try:
            email_account = self.request.user.emails.get(email=selected_email)
            return email_account.email_boxes.all()
        except Email.DoesNotExist:
            raise exceptions.PermissionDenied({"error": "Invalid email selected."})


class MailboxEmailTrashView(generics.UpdateAPIView):
    serializer_class = MailboxTrashSerializer

    def update(self, request, *args, **kwargs):
        selected_email = self.request.query_params.get("email")
        move_to_trash = request.query_params.get("move_to_trash")
        if not selected_email:
            raise exceptions.ValidationError(
                {"error": "No email provided in the query parameters."}
            )
        if move_to_trash is None:
            raise exceptions.ValidationError(
                {"error": "'move_to_trash' flag is required in the query parameters."}
            )

        try:
            email_account = self.request.user.emails.get(email=selected_email)
        except Email.DoesNotExist:
            raise exceptions.PermissionDenied({"error": "Invalid email selected."})

        serializer = self.get_serializer(
            data=request.data, context={"request": request, "email": email_account}
        )
        if serializer.is_valid():
            if move_to_trash.lower() == "true":
                serializer.update_emails_to_trash()
                return Response(
                    {"message": "Emails moved to trash successfully"},
                    status=status.HTTP_200_OK,
                )
            elif move_to_trash.lower() == "false":
                serializer.update_trash_to_emails()
                return Response(
                    {"message": "Emails restored from trash successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "'move_to_trash' must be either 'true' or 'false'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
