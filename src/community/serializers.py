from rest_framework import serializers

from community.models import Board, Comment


class BoardSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    market = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    is_mine = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Board
        fields = (
            "id",
            "email",
            "market",
            "title",
            "content",
            "comment_count",
            "like_count",
            "is_liked",
            "is_mine",
            "username",
            "created_at",
        )
        read_only_fields = (
            "id",
            "email",
            "market",
            "comment_count",
            "like_count",
            "is_liked",
            "is_mine",
            "username",
            "created_at",
        )

    def get_email(self, obj: Board) -> str:
        return obj.user.email

    def get_market(self, obj: Board) -> str:
        return obj.market.market

    def get_comment_count(self, obj: Board) -> int:
        return obj.comment.count()

    def get_like_count(self, obj: Board) -> int:
        return obj.like.count()

    def get_is_liked(self, obj: Board) -> bool:
        return (
            True
            if obj.like.filter(user=self.context["request"].user).exists()
            else False
        )

    def get_is_mine(self, obj: Board) -> bool:
        return obj.user == self.context["request"].user

    def get_username(self, obj: Board) -> str:
        return obj.user.username

    def get_created_at(self, obj: Board) -> str:
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")


class CommentSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "email", "comment")

    def get_email(self, obj: Comment) -> str:
        return obj.user.email


class BoardDetailSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    market = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    comment = CommentSerializer(many=True)
    is_mine = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Board
        fields = (
            "id",
            "email",
            "market",
            "title",
            "content",
            "comment",
            "like_count",
            "is_mine",
            "username",
            "created_at",
        )

    def get_email(self, obj: Board) -> str:
        return obj.user.email

    def get_market(self, obj: Board) -> str:
        return obj.market.market

    def get_like_count(self, obj: Board) -> int:
        return obj.like.count()

    def get_is_mine(self, obj: Board) -> bool:
        return obj.user == self.context["request"].user

    def get_username(self, obj: Board) -> str:
        return obj.user.username

    def get_created_at(self, obj: Board) -> str:
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
