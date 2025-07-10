from django.db import models
from django.db.models import QuerySet

from user.models import User
from core.models import BaseModel


class Board(BaseModel):
    title = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment: "QuerySet[Comment]"

    class Meta:
        db_table = "board"


class Comment(BaseModel):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="comment"
    )

    class Meta:
        db_table = "comment"