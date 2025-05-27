from django.urls import path

# from community.views.my import MyAccountView
from community.views.board import (
    BoardPostListCreateAPIView,
    BoardPostDetailAPIView,
)

urlpatterns = [
    # path("my", MyAccountView.as_view()),

    path("posts/", BoardPostListCreateAPIView.as_view()),

    path("posts/<int:pk>/", BoardPostDetailAPIView.as_view()),
]
