from django.urls import path

from community.views.board import BoardView, BoardDetailView

urlpatterns = [
    path("/<str:market>", BoardView.as_view()),
    path("/<str:market>/<int:board_id>", BoardDetailView.as_view()),
]
