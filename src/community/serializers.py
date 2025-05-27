from rest_framework import serializers

from community.models import BoardPost

class BoardPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardPost
        fields = ("id", "title", "content", "created_at", "updated_at", "author")
        read_only_fields = ("id", "created_at", "updated_at", "author")
        
    def create(self, validated_data):
        # Create a new BoardPost instance with the validated data
        return BoardPost.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update the instance with the validated data
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance     
