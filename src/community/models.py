from django.db import models
from user.models import User
from core.models import BaseModel

# Create your models here.
class BoardPost(BaseModel):
    title = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title