from django.contrib import admin
from django.utils.html import format_html
from NeuroMail.models import Email, EmailAttachment, EmailRecipient


class EmailAttachmentInline(admin.TabularInline):
    model = EmailAttachment
    extra = 0  # No extra empty rows
    fields = ("filename", "content_type")
    readonly_fields = ("filename", "content_type")
    show_change_link = True


class EmailRecipientInline(admin.TabularInline):
    model = EmailRecipient
    extra = 0  # No extra empty rows
    fields = ("email", "name", "recipient_type")
    readonly_fields = ("email", "name", "recipient_type")
    show_change_link = True


class EmailAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "email_type",
        "primary_email_type",
        "mailbox",
        "is_starred",
        "is_seen",
        "total_size",
        "mailbox_email",
    )

    def mailbox_email(self, obj):
        return format_html(
            "<a href='mailto:{}'>{}</a>", obj.mailbox.email, obj.mailbox.email
        )

    mailbox_email.short_description = "Mailbox Email"

    search_fields = ("id", "subject", "email_type", "mailbox__email")
    list_filter = ("email_type", "is_starred", "is_seen")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject",
                    "body",
                    "email_type",
                    "primary_email_type",
                    "is_starred",
                    "is_seen",
                    "total_size",
                    "mailbox",
                ),
            },
        ),
    )

    readonly_fields = ("total_size",)
    actions = ["mark_as_seen", "mark_as_starred"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def mark_as_seen(self, request, queryset):
        queryset.update(is_seen=True)

    mark_as_seen.short_description = "Mark selected emails as seen"

    def mark_as_starred(self, request, queryset):
        queryset.update(is_starred=True)

    mark_as_starred.short_description = "Mark selected emails as starred"

    inlines = [EmailAttachmentInline, EmailRecipientInline]


# Register the model with the custom admin class
admin.site.register(Email, EmailAdmin)
