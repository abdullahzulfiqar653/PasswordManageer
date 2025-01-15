from django.db import models

from main.models.abstract.base import BaseModel


class SharedAccess(BaseModel):
    class Permission(models.TextChoices):
        READ = "read", "Read"
        WRITE = "write", "Write"
        FULL = "full", "Full"

    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="shared_accesses"
    )
    item = models.ForeignKey(
        "NeuroDrive.File", on_delete=models.CASCADE, related_name="shared_accesses"
    )
    permission_type = models.CharField(
        max_length=50, choices=Permission.choices, default=Permission.FULL
    )

    def __str__(self):
        return f"{self.user.username} - {self.permission_type}"
