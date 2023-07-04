from django.db import models


class User(models.Model):
    user_id = models.IntegerField(primary_key=False)
    username = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=100)
