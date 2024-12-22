from rest_framework import generics

from NeuroDrive.models.directory import Directory
from NeuroDrive.serializers.directory import DirectorySerializer


class DirectoryListCreateView(generics.ListCreateAPIView):
    serializer_class = DirectorySerializer

    def get_queryset(self):
        return (
            self.request.user.directories.filter(parent=None, name="main")
            | Directory.objects.filter(shared_with=self.request.user)
        ).order_by("created_at")


class DirectoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.request.user.directories.all() | Directory.objects.filter(
                shared_with=self.request.user
            )
        return Directory.objects.none()

    def get_object(self):
        if not self.kwargs["pk"] == "main":
            obj = super().get_object()
        obj, _ = Directory.objects.get_or_create(owner=self.request.user, name="main")
        return obj

    def perform_destroy(self, instance):
        if not instance.name == "main":
            instance.delete()
