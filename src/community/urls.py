from django.urls import path

# from community.views.my import MyAccountView
from community.views.board import (
    BoardPostListCreateAPIView,
    BoardPostDetailAPIView,
)

urlpatterns = [

    path("/post", BoardPostListCreateAPIView.as_view()),

    path("/post/<int:pk>", BoardPostDetailAPIView.as_view()),
]
