from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from NeuroMail.models import MailBox, Email


class IsMailBoxOwner(BasePermission):
    """
    Custom permission to check if the user owns the mailbox they are trying to access.
    """

    def has_permission(self, request, view):
        # Check if the URL contains a 'mailbox_id' parameter
        mailbox_id = view.kwargs.get("mailbox_id") or view.kwargs.get("pk")
        if mailbox_id:
            try:
                mailbox = MailBox.objects.get(id=mailbox_id)
                # Attach mailbox instance to request if user is the owner
                if mailbox.user == request.user:
                    request.mailbox = mailbox
                    return True
                else:
                    raise PermissionDenied("You do not own this mailbox.")
            except MailBox.DoesNotExist:
                raise PermissionDenied("Mailbox not found.")
        return True  # If no mailbox_id in URL, allow access


class IsEmailOwner(BasePermission):
    """
    Custom permission to check if the user owns the mailbox they are trying to access.
    """

    def has_permission(self, request, view):
        # Check if the URL contains a 'email_id' parameter
        email_id = view.kwargs.get("email_id") or view.kwargs.get("pk")
        if email_id:
            try:
                email = Email.objects.get(id=email_id)
                if email.mailbox.user == request.user:
                    request.email = email
                    return True
                else:
                    raise PermissionDenied("You do not own this mailbox.")
            except MailBox.DoesNotExist:
                raise PermissionDenied("Mailbox not found.")
        return True
