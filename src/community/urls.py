from django.urls import path

# from community.views.my import MyAccountView
from community.views.board import (
    BoardPostListCreateAPIView,
    BoardPostDetailAPIView,
)

from community.views.comment import (
    BoardCommentListAPIView,
    BoardCommentCreateAPIView,
)

urlpatterns = [

    path("/post", BoardPostListCreateAPIView.as_view()),
    path("/post/<int:pk>", BoardPostDetailAPIView.as_view()),
    
    path("/post/<int:post_id>/comment", BoardCommentCreateAPIView.as_view()),  # 특정 게시글에 댓글 작성
]
