from rest_framework import serializers

from NeuroMail.models.mailbox import MailBox


class MailboxTrashSerializer(serializers.Serializer):
    mailboxes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=MailBox.objects.none(), pk_field=serializers.CharField()
    )

    def __init__(self, *args, **kwargs):
        """
        Modifying the queryset of the emails field based on the request user.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if hasattr(request, "user") and request.user.is_authenticated:
            email = self.context.get("email")
            for i in email.email_boxes.all():
                print(i.id, "-----------")
            self.fields["mailboxes"].queryset = email.email_boxes.all()

    def update_emails_to_trash(self):
        emails = self.validated_data["emails"]

        mailboxes_to_update = []
        for email in emails:
            email.email_type = MailBox.TRASH
            mailboxes_to_update.append(email)

        if mailboxes_to_update:
            MailBox.objects.bulk_update(mailboxes_to_update, ["email_type"])
        return emails

    def update_trash_to_emails(self):
        emails = self.validated_data["emails"]
        mailboxes_to_update = []
        for email in emails:
            if email.email_type == MailBox.TRASH:
                email.email_type == email.primary_email_type
                mailboxes_to_update.append(email)

        if mailboxes_to_update:
            MailBox.objects.bulk_update(mailboxes_to_update, ["email_type"])
        return emails
