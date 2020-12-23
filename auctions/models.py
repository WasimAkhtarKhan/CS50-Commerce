from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    basebid = models.IntegerField()
    owner = models.CharField(max_length=64)
    currentbid = models.IntegerField()
    imglink = models.CharField(max_length=200)
    category = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)

class Bid(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    currentbid = models.IntegerField()

class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.TextField()
    listingid = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()


class Closedbid(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winprice = models.IntegerField()

class Alllisting(models.Model):
    listingid = models.IntegerField()
    title = models.CharField(max_length=64)
    description = models.TextField()
    link = models.CharField(max_length=64,default=None,blank=True,null=True)
