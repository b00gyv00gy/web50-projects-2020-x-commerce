from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    
    #class Category(models.TextChoices):
    #    FASION = 'Fasion'
    #    TOYS = 'Toys'
    #    ELECTRONICS = 'Electronics'
    #    HOME = 'Home'
    
    title = models.CharField(max_length=64, default="empty")
    description = models.TextField()
    bid = models.FloatField(default="0")
    imgURL = models.URLField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="%(class)s_foo")
    last_bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="%(class)s_bar")
    status = models.BooleanField(default=True)
    #category = models.TextChoices(choices=Category.choices)

class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

