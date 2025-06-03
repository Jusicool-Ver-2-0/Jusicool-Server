from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from community.models import BoardPost, BoardComment
from community.serializers import BoardCommentSerializer
from core.authentications import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated

class BoardCommentListAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        post = get_object_or_404(BoardPost, id=post_id)
        comments = post.comments.all()
        serializer = BoardCommentSerializer(comments, many=True)
        return Response(serializer.data)

class BoardCommentCreateAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        post = get_object_or_404(BoardPost, id=post_id)
        serializer = BoardCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
