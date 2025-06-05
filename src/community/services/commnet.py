# services/comment.py

from django.shortcuts import get_object_or_404
from community.models import BoardPost, BoardComment

class BoardCommentService:

    @staticmethod
    def get_post(post_id):
        return get_object_or_404(BoardPost, id=post_id)

    @staticmethod
    def list_comments(post):
        return post.comments.all()

    @staticmethod
    def create_comment(data, user, post):
        comment = BoardComment(**data, user=user, post=post)
        comment.save()
        return comment
