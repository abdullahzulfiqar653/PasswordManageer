import os

from rest_framework.views import APIView

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse, Http404, HttpResponseForbidden

from NeuroMail.models import EmailAttachment
from PasswordManager.models import Password


FILE_MODEL_MAP = {
    "mailbox-attachments": {
        "model": EmailAttachment,
        "path": "protected/mailbox/attachments/",
    },
    "password-attachments": {
        "model": Password,
        "path": "protected/passwords/attachments/",
    },
}


class ProtectedMediaView(APIView):
    """
    View to serve protected media files with token-based authentication.
    Checks if the user owns the media file and serves it.
    """

    def get(self, request, file_type, file_name):
        file_type = FILE_MODEL_MAP.get(file_type)
        Model = file_type["model"]
        if not Model:
            raise Http404("Invalid file type or Media not found.")

        try:
            obj = Model.objects.get(file=f"{file_type['path']}{file_name}")
        except Model.DoesNotExist:
            raise Http404("Invalid file type or Media not found.")

        error_msg_403 = "You do not have permission to access this media."
        if hasattr(obj, "mail"):
            if request.user != obj.mail.mailbox.user:
                return HttpResponseForbidden(error_msg_403)

        elif hasattr(obj, "user"):
            if request.user != obj.user:
                return HttpResponseForbidden(error_msg_403)

        else:
            return HttpResponseForbidden("Invalid permission check configuration.")

        # Construct the full file path in the protected directory
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_type["path"], file_name)

        if not os.path.exists(full_file_path):
            raise Http404("File not found.")

        file_handle = default_storage.open(full_file_path, "rb")
        return FileResponse(file_handle, content_type=obj.content_type)
