from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "content", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]

class SearchSerializer(serializers.Serializer):
    question = serializers.CharField()