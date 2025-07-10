from django.shortcuts import get_object_or_404
from django.db import transaction
from community.models import Board, Comment


class BoardCommentService:

    @staticmethod
    def get_post(post_id):
        return get_object_or_404(Board, id=post_id)

    @staticmethod
    def list_comments(post_id):
        post = get_object_or_404(Board, id=post_id)
        return post.comments.all()

    @staticmethod
    @transaction.atomic
    def create_comment(data, user, post):
        comment = Comment(user=user, post=post, **data)
        comment.save()
        return comment

    @staticmethod
    @transaction.atomic
    def update_comment(comment_id, data):
        comment = get_object_or_404(Comment, id=comment_id)
        for attr, value in data.items():
            setattr(comment, attr, value)
        comment.save()
        return comment
