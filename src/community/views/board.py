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
from rest_framework.permissions import IsAuthenticated
from core.authentications import CsrfExemptSessionAuthentication

class BoardPostListCreateAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    def get(self, request: Request):
        posts = BoardPost.objects.all()
        serializer = BoardPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = BoardPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardPostDetailAPIView(APIView):
    
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    def get(self, request: Request, pk: int):
        post = get_object_or_404(BoardPost, pk=pk)
        serializer = BoardPostSerializer(post)
        return Response(serializer.data)

    def put(self, request: Request, pk: int):
        if request.user != post.user:
            return Response({"detail": "권한이 없습니다."}, status=403)
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
