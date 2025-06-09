from django.shortcuts import get_object_or_404
from django.db import transaction
from community.models import BoardPost, BoardComment

class BoardCommentService:

    @staticmethod
    def get_post(post_id):
        return get_object_or_404(BoardPost, id=post_id)

    @staticmethod
    def list_comments(post):
        return post.comments.all()

    @staticmethod
    @transaction.atomic
    def create_comment(data, user, post):
        comment = BoardComment(user=user, post=post, **data)
        comment.save()
        return comment

    @staticmethod
    @transaction.atomic
    def update_comment(comment_id, data):
        comment = get_object_or_404(BoardComment, id=comment_id)
        for attr, value in data.items():
            setattr(comment, attr, value)
        comment.save()
        return comment
