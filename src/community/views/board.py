# views/board.py

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.authentications import CsrfExemptSessionAuthentication
from community.serializers import BoardPostSerializer
from services.board import BoardPostService

class BoardPostListCreateAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        posts = BoardPostService.list_posts()
        serializer = BoardPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = BoardPostSerializer(data=request.data)
        if serializer.is_valid():
            post = BoardPostService.create_post(serializer.validated_data, request.user)
            return Response(BoardPostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardPostDetailAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, pk: int):
        post = BoardPostService.get_post(pk)
        serializer = BoardPostSerializer(post)
        return Response(serializer.data)

    def put(self, request: Request, pk: int):
        post = BoardPostService.get_post(pk)
        if request.user != post.user:
            return Response({"detail": "권한이 없습니다."}, status=403)

        serializer = BoardPostSerializer(post, data=request.data)
        if serializer.is_valid():
            updated_post = BoardPostService.update_post(post, serializer.validated_data)
            return Response(BoardPostSerializer(updated_post).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int):
        post = BoardPostService.get_post(pk)
        if request.user != post.user:
            return Response({"detail": "권한이 없습니다."}, status=403)
        BoardPostService.delete_post(post)
        return Response(status=status.HTTP_204_NO_CONTENT)
