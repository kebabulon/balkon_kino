from django.utils import timezone
from django.db import models
from django.conf import settings


# TODO: maybe add Actor/Director model?


class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"{self.title}"


class Subscription(models.Model):
    SUBSCRIPTION_PLAN = {
        "1": "Basic",
        "2": "Pro",
        "3": "Ultra Mega Pro++ Premium",
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription_plan = models.CharField(
        max_length=1,
        choices=SUBSCRIPTION_PLAN,
    )
    expiration_date = models.DateTimeField()


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlist")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["user", "movie"]
