# services/board.py

from community.models import BoardPost
from django.db import transaction
from django.shortcuts import get_object_or_404
from community.serializers import BoardPostSerializer  


class BoardPostService:

    @staticmethod
    def list_posts():
        return BoardPost.objects.all()

    @staticmethod
    @transaction.atomic
    def create_post(serializer, user):
        serializer.is_valid(raise_exception=True)
        return serializer.save(user=user)

    @staticmethod
    def get_post(pk, user):
        return get_object_or_404(BoardPost, pk=pk, user=user)

    @staticmethod
    @transaction.atomic
    def update_post(serializer):
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    @transaction.atomic
    def delete_post(post):
        post.delete()
