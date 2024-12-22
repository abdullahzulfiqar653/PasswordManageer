from rest_framework import serializers

from NeuroDrive.models.directory import Directory
from NeuroDrive.serializers.file import FileSerializer


class ChildDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = ["id", "name", "files", "shared_with", "parent"]
        read_only_fields = ["shared_with"]


class DirectorySerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    children = ChildDirectorySerializer(many=True, read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Directory.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Directory
        fields = ["id", "name", "files", "shared_with", "children", "parent"]
        read_only_fields = ["shared_with", "children"]
        depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if hasattr(request, "user") and request.user.is_authenticated:
            self.fields["parent"].queryset = request.user.directories.all()

    def validate(self, data):
        owner = self.context["request"].user
        name = data.get("name")
        parent = data.get("parent")

        if Directory.objects.filter(owner=owner, name=name, parent=parent).exists():
            raise serializers.ValidationError(
                "A directory with this name already exists."
            )

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if not validated_data.get("parent"):
            obj, _ = Directory.objects.get_or_create(name="main", owner=request.user)
            validated_data["parent"] = obj
        validated_data["owner"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("parent"):
            del validated_data["parent"]
        return super().update(instance, validated_data)
