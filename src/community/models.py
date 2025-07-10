from django.db import models
from django.db.models import QuerySet

from market.models import Market
from user.models import User
from core.models import BaseModel


class Board(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="board")

    title = models.CharField(max_length=50)
    content = models.TextField()

    class Meta:
        db_table = "board"


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="comment")

    comment = models.TextField()

    class Meta:
        db_table = "comment"
