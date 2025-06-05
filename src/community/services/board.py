# services/board.py

from community.models import BoardPost
from django.shortcuts import get_object_or_404

class BoardPostService:

    @staticmethod
    def list_posts():
        return BoardPost.objects.all()

    @staticmethod
    def create_post(data, user):
        post = BoardPost(**data, user=user)
        post.save()
        return post

    @staticmethod
    def get_post(pk):
        return get_object_or_404(BoardPost, pk=pk)

    @staticmethod
    def update_post(post, data):
        for key, value in data.items():
            setattr(post, key, value)
        post.save()
        return post

    @staticmethod
    def delete_post(post):
        post.delete()
