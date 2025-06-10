# views/comment.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.authentications import CsrfExemptSessionAuthentication
from community.serializers import BoardCommentSerializer
from community.services.comment import BoardCommentService

class BoardCommentListAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        comments = BoardCommentService.list_comments(post_id)
        serializer = BoardCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardCommentCreateAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        post = BoardCommentService.get_post(post_id)
        serializer = BoardCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        comment = BoardCommentService.create_comment(serializer.validated_data, request.user, post)
        
        response_serializer = BoardCommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

