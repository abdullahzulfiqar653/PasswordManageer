import json

from api.models.note import Note
from api.ai.embedder import embedder
from api.models.feature import Feature
from api.models.takeaway import Takeaway
from api.models.takeaway_type import TakeawayType

from django.conf import settings
from rest_framework import exceptions
from rest_framework import serializers


class DefaultSourcesCreateSerializer(serializers.Serializer):
    def create(self, validated_data):
        request = self.context.get("request")
        workspace = request.project.workspace
        notes_limit = workspace.get_feature_value(
            Feature.Code.NUMBER_OF_KNOWLEDGE_SOURCES
        )
        if workspace.notes.count() >= notes_limit:
            raise exceptions.PermissionDenied(
                f"You have reached the limit of {notes_limit} Knowledge sources."
            )
        try:
            with open(
                f"{settings.BASE_DIR}/api/fixtures/dummy_knowledge_source.json", "r"
            ) as file:
                knowledge_sources = json.load(file)
            with open(
                f"{settings.BASE_DIR}/api/fixtures/dummy_takeaways.json", "r"
            ) as file:
                take_aways = json.load(file)
        except:
            serializers.ValidationError(
                "Something bad happend while adding knowledge sources."
            )
        takeaway_types = TakeawayType.objects.filter(project=request.project)
        takeaway_type_dict = {
            takeaway_type.name: takeaway_type.id for takeaway_type in takeaway_types
        }
        notes_list = []
        takeaways_list = []
        for source in knowledge_sources:
            fields = source["fields"]
            note = Note(
                title=fields["title"],
                author=request.user,
                project=request.project,
                workspace=workspace,
                description=fields["description"],
                content=fields["content"],
                summary=fields["summary"],
            )
            notes_list.append(note)
            for type, values in take_aways.items():
                takeaway_type = TakeawayType.objects.filter(
                    name=type, project=request.project
                ).first()
                takeaway_type_id = takeaway_type_dict.get(type)
                for value in values:
                    takeaways_list.append(
                        Takeaway(
                            title=value,
                            type_id=takeaway_type_id,
                            created_by=request.user,
                            note=note,
                            vector=embedder.embed_documents([value])[0],
                        )
                    )
        Note.objects.bulk_create(notes_list)
        Takeaway.objects.bulk_create(takeaways_list)
        return {}
