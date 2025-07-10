from community.models import Board, Comment, BoardLike
from django.db import transaction
from django.shortcuts import get_object_or_404
from community.serializers import BoardSerializer, CommentSerializer
from market.models import Market
from user.models import User


class BoardService:

    def get_board_list_by_market(self, market: str):
        return Board.objects.filter(market__market=market)

    @transaction.atomic
    def create(self, user: User, market: str, serializer: BoardSerializer):
        Board.objects.create(
            user=user,
            market=get_object_or_404(Market, market=market),
            **serializer.validated_data
        )

    def get_board_detail(self, market: str, board_id: int):
        return get_object_or_404(Board, id=board_id, market__market=market)

    @transaction.atomic
    def create_comment(
        self, user: User, market, board_id, serializer: CommentSerializer
    ):
        Comment.objects.create(
            user=user,
            board=get_object_or_404(Board, id=board_id, market__market=market),
            **serializer.validated_data
        )

    @transaction.atomic
    def like(self, user: User, market: str, board_id: int):
        board = get_object_or_404(Board, id=board_id, market__market=market)
        if board.like.filter(user=user).exists():
            board.like.filter(user=user).delete()
        else:
            BoardLike.objects.create(user=user, board=board)
