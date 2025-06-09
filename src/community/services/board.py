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
    def create_post(data, user):
        serializer = BoardPostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save(user=user)

    @staticmethod
    def get_post(pk):
        return get_object_or_404(BoardPost, pk=pk)

    @staticmethod
    @transaction.atomic
    def update_post(pk, data):
        post = get_object_or_404(BoardPost, pk=pk)
        serializer = BoardPostSerializer(post, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    @transaction.atomic
    def delete_post(pk):
        post = get_object_or_404(BoardPost, pk=pk)
        post.delete()
