from django.db import models
from users.models import User


class Post(models.Model):
    user_id = models.IntegerField()
    post_id = models.IntegerField(primary_key=True, default=0)
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

