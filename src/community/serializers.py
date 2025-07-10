from rest_framework import serializers

from community.models import Board, Comment


class BoardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("id", "post", "user", "comment")
        read_only_fields = ("id", "post", "user")


class BoardPostSerializer(serializers.ModelSerializer):
    comments = BoardCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "title", "content", "user", "comments")
        read_only_fields = ("id", "user")
