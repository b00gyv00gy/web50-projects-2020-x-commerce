from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64, default="empty")
    description = models.TextField()
    bid = models.FloatField(default="0")
    imgURL = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
