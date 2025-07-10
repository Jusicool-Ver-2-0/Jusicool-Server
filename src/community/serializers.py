from rest_framework import serializers

from community.models import BoardPost, BoardComment


class BoardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardComment
        fields = ("id", "post", "user", "comment")
        read_only_fields = ("id", "post", "user")


class BoardPostSerializer(serializers.ModelSerializer):
    comments = BoardCommentSerializer(many=True, read_only=True)

    class Meta:
        model = BoardPost
        fields = ("id", "title", "content", "user", "comments")
        read_only_fields = ("id", "user")
