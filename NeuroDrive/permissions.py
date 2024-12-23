from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from NeuroDrive.models.file import File
from NeuroDrive.models.directory import Directory


class IsDirectoryOwner(BasePermission):
    """
    Custom permission to check if the user owns the directory they are trying to access.
    """

    def has_permission(self, request, view):
        # Check if the URL contains a 'directory_id' parameter
        directory_id = view.kwargs.get("directory_id") or view.kwargs.get("pk")

        if directory_id:
            directory = get_object_or_404(Directory, id=directory_id)
            # Attach directory instance to request if user is the owner
            if directory.owner == request.user:
                request.directory = directory
                return True
            else:
                raise PermissionDenied("You do not own this directory.")


class IsOwnerOrSharedDirectory(BasePermission):
    """
    Custom permission to check if the user is the owner of the directory or
    if the directory is shared with the user.
    """

    def has_permission(self, request, view):
        directory_id = view.kwargs.get("directory_id") or view.kwargs.get("pk")
        if directory_id:
            # Efficiently fetch the directory with the user's ownership or shared status.
            directory = get_object_or_404(Directory, id=directory_id)

            # Check if the current user is the owner or is listed in the shared_with.
            user = request.user
            if directory.owner == user or user in directory.shared_with.all():
                request.directory = directory
                return True
            return False


class IsFileOwner(BasePermission):
    """
    Custom permission to check if the user owns the file.
    """

    def has_permission(self, request, view):
        file_id = view.kwargs.get("file_id") or view.kwargs.get("pk")
        if file_id:
            # Efficiently fetch the directory with the user's ownership or shared status.
            file = get_object_or_404(File, id=file_id)
            # Check if the current user is the owner or is listed in the shared_with.
            user = request.user
            if file.owner == user:
                request.file = file
                return True
            return False
