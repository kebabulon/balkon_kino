from django.db import models
from django.conf import settings


# TODO: maybe add Actor/Director model?


class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)


class Movie(models.Model):
    MATURITY_RATINGS = {
        "G": "General Audiences",
        "PG": "Parental Guidance Suggested",
        "PG-13": "Parents Strongly Cautioned",
        "R": "Restricted",
        "NC-17": "Adults only",
    }

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    release_date = models.PositiveIntegerField()
    maturity_rating = models.CharField(
        max_length=5,
        choices=MATURITY_RATINGS,
    )
    runtime = models.DurationField()
    genres = models.ManyToManyField(Genre)


# TODO: create Subscription model
# class Subscription(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
