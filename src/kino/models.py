from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)


class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)


# TODO: create Subscription model
# class Subscription(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
