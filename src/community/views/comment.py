# views/comment.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.authentications import CsrfExemptSessionAuthentication
from community.serializers import BoardCommentSerializer
from services.commnet import BoardCommentService

class BoardCommentListAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        post = BoardCommentService.get_post(post_id)
        comments = BoardCommentService.list_comments(post)
        serializer = BoardCommentSerializer(comments, many=True)
        return Response(serializer.data)

class BoardCommentCreateAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        post = BoardCommentService.get_post(post_id)
        serializer = BoardCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = BoardCommentService.create_comment(serializer.validated_data, request.user, post)
            return Response(BoardCommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
