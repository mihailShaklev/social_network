from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    username = models.CharField(max_length=64, default="NAME")
    text = models.TextField()
    time_stamp = models.DateTimeField()
    likes = models.IntegerField()


class Followers(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    like = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="liked_posts")