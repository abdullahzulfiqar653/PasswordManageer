from django.db import models

from main.models.abstract.base import BaseModel
from NeuroDrive.models.shared_access import SharedAccess


class Directory(BaseModel):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="directories"
    )
    parent = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, related_name="children"
    )
    shared_with = models.ManyToManyField("auth.User", related_name="shared_directories")

    def share_folder(self, user):
        self.shared_with.add(user)
        for file in self.files.all():
            SharedAccess.objects.create(
                user=user, item=file, permission_type=SharedAccess.READ
            )
        for subfolder in self.subfolders.all():
            subfolder.share_folder(user)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("owner", "name", "parent")
