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
        serializer.is_valid(raise_exception=True)
        post = BoardPostService.create_post(serializer.validated_data, request.user)
        return Response(BoardPostSerializer(post).data, status=status.HTTP_201_CREATED)

class BoardPostDetailAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, pk: int):
        post = BoardPostService.get_post(pk)
        serializer = BoardPostSerializer(post)
        return Response(serializer.data)

    def put(self, request: Request, pk: int):
        post = BoardPostService.get_post(pk,request.user)

        serializer = BoardPostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_post = BoardPostService.update_post(post, serializer.validated_data)
        return Response(BoardPostSerializer(updated_post).data)
  

    def delete(self, request: Request, pk: int):
        post = BoardPostService.get_post(pk,request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

