from django.db import models

from main.models.abstract.base import BaseModel


class File(BaseModel):
    name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    owner = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="files"
    )
    directory = models.ForeignKey(
        "NeuroDrive.Directory",
        null=True,
        on_delete=models.CASCADE,
        related_name="files",
    )
    size = models.PositiveIntegerField()  # Size in bytes
    content = models.FileField(upload_to="protected/neurodrive/")

    def __str__(self):
        return self.name

    def move_to_folder(self, new_folder):
        """Move file to another folder"""
        self.folder = new_folder
        self.save()

    class Meta:
        unique_together = ("owner", "name", "directory")
