from rest_framework import serializers

from community.models import BoardPost, BoardComment

class BoardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardComment
        fields = ("id", "post", "user", "comment")
        read_only_fields = ("id", "post", "user")
        
    def create(self, validated_data):
        # Create a new BoardComment instance with the validated data
        return BoardComment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update the instance with the validated data
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance

class BoardPostSerializer(serializers.ModelSerializer):
    comments = BoardCommentSerializer(many=True, read_only=True)
    class Meta:
        model = BoardPost
        fields = ("id", "title", "content", "user","comments")
        read_only_fields = ("id", "user")
        
    def create(self, validated_data):
        # Create a new BoardPost instance with the validated data
        return BoardPost.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update the instance with the validated data
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance     

     

