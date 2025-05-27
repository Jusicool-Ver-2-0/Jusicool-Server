from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from community.models import BoardPost
from community.serializers import BoardPostSerializer
from django.shortcuts import get_object_or_404

class BoardPostListCreateAPIView(APIView):
    def get(self, request: Request):
        posts = BoardPost.objects.all()
        serializer = BoardPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = BoardPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # 인증된 사용자 기반
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardPostDetailAPIView(APIView):
    def get(self, request: Request, pk: int):
        post = get_object_or_404(BoardPost, pk=pk)
        serializer = BoardPostSerializer(post)
        return Response(serializer.data)

    def put(self, request: Request, pk: int):
        post = get_object_or_404(BoardPost, pk=pk)
        serializer = BoardPostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int):
        post = get_object_or_404(BoardPost, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
