from django.contrib import admin
from NeuroMail.models.email import Email
from django.utils.html import format_html


class EmailAdmin(admin.ModelAdmin):
    # List view customization
    list_display = (
        "subject",
        "email_type",
        "primary_email_type",
        "mailbox",
        "is_starred",
        "is_seen",
        "total_size",
        "mailbox_email",
    )

    # Adding a custom method to display mailbox email
    def mailbox_email(self, obj):
        return format_html(
            "<a href='mailto:{}'>{}</a>", obj.mailbox.email, obj.mailbox.email
        )

    mailbox_email.short_description = "Mailbox Email"

    # Fields that are searchable in the admin list view
    search_fields = ("subject", "email_type", "mailbox__email")

    # Adding filters in the sidebar for easier navigation
    list_filter = ("email_type", "is_starred", "is_seen")

    # Fields that are displayed on the detail view/edit page
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

    # Read-only fields
    readonly_fields = ("total_size",)

    # Customize form to make sure specific fields are displayed in a particular order
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    # Optionally, you can add a method for actions like marking emails as seen or starred
    actions = ["mark_as_seen", "mark_as_starred"]

    def mark_as_seen(self, request, queryset):
        queryset.update(is_seen=True)

    mark_as_seen.short_description = "Mark selected emails as seen"

    def mark_as_starred(self, request, queryset):
        queryset.update(is_starred=True)

    mark_as_starred.short_description = "Mark selected emails as starred"


# Register the model with the custom admin class
admin.site.register(Email, EmailAdmin)
