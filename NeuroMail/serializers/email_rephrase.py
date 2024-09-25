from rest_framework import serializers
from NeuroMail.models.email_ai_template import EmailAiTemplate
from main.ai.generators.email_template_text_generator import generate_email_message


class RephraseEmailCreateSerializer(serializers.Serializer):
    email_text = serializers.CharField()
    template = serializers.PrimaryKeyRelatedField(
        queryset=EmailAiTemplate.objects.all(), write_only=True
    )

    def create(self, validated_data):
        template = validated_data["template"]
        email_text = validated_data["email_text"]
        try:
            rephrased = generate_email_message(template.name, email_text)
        except:  # noqa
            raise serializers.ValidationError(
                {"error": "Failed to rephrase, please try again."}
            )

        return {"email_text": rephrased}
