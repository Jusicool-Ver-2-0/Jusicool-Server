from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from community.serializers import (
    BoardSerializer,
    CommentSerializer,
    BoardDetailSerializer,
)
from core.authentications import CsrfExemptSessionAuthentication
from community.services.board import BoardService


class BoardView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    board_service = BoardService()

    def get(self, request: Request, market: str) -> Response:
        boards = self.board_service.get_board_list_by_market(market)
        serializer = BoardSerializer(boards, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, market: str) -> Response:
        serializer = BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.board_service.create(
            user=request.user, market=market, serializer=serializer
        )
        return Response(status=status.HTTP_201_CREATED)


class BoardDetailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    board_service = BoardService()

    def get(self, request: Request, market: str, board_id: int) -> Response:
        board = self.board_service.get_board_detail(market, board_id)
        serializer = BoardDetailSerializer(board, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 작성
    def post(self, request: Request, market: str, board_id: int) -> Response:
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.board_service.create_comment(
            user=request.user, market=market, board_id=board_id, serializer=serializer
        )
        return Response(status=status.HTTP_201_CREATED)

    # 게시글 수정
    def put(self, request: Request, market: str, board_id: int) -> Response:
        serializer = BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.board_service.update(
            user=request.user, market=market, board_id=board_id, serializer=serializer
        )
        return Response(status=status.HTTP_200_OK)

    # 좋아요 토글
    def patch(self, request: Request, market: str, board_id: int) -> Response:
        self.board_service.like(user=request.user, market=market, board_id=board_id)
        return Response(status=status.HTTP_200_OK)

    # 게시글 삭제
    def delete(self, request: Request, market: str, board_id: int) -> Response:
        self.board_service.delete(user=request.user, market=market, board_id=board_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
