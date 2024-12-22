from django.db import models

from main.models.abstract.base import BaseModel


class SharedAccess(BaseModel):
    READ = "read"
    WRITE = "write"
    FULL = "full"
    PERMISSION_CHOICES = [
        (READ, "Read"),
        (WRITE, "Write"),
        (FULL, "Full"),
    ]

    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="shared_accesses"
    )
    item = models.ForeignKey(
        "NeuroDrive.File", on_delete=models.CASCADE, related_name="shared_accesses"
    )
    permission_type = models.CharField(max_length=50, choices=PERMISSION_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.permission_type}"
