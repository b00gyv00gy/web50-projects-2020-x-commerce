from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64, default="empty")
    description = models.CharField(max_length=64, default="empty")
    starting_bid = models.FloatField(default="0")
    imgURL = models.URLField(default="https://harrypotter.fandom.com/wiki/Broomstick?file=Hpnbbrbkmk-w370.jpg")
    #user = models.ForeignKey(User, on_delete=models.CASCADE)

class Bid(models.Model):
    bid = models.FloatField()
    

class Comment(models.Model):
    comment = models.CharField(max_length=64, default="empty")