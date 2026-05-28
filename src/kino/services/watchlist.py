from __future__ import annotations

from django.db import transaction

from kino.domain.errors import (
    MovieNotFound,
    WatchlistAlreadyContainsMovie,
    WatchlistItemNotFound,
    WatchlistMovieRequired,
)
from kino.models import Movie, Watchlist


def _resolve_movie(movie_or_movie_id):
    if movie_or_movie_id is None:
        raise WatchlistMovieRequired()

    if isinstance(movie_or_movie_id, Movie):
        return movie_or_movie_id

    try:
        return Movie.objects.get(pk=movie_or_movie_id)
    except Movie.DoesNotExist as exc:
        raise MovieNotFound() from exc


@transaction.atomic
def add_movie_to_watchlist(*, user, movie):
    movie_instance = _resolve_movie(movie)
    watchlist_item, created = Watchlist.objects.get_or_create(
        user=user,
        movie=movie_instance,
    )

    if not created:
        raise WatchlistAlreadyContainsMovie()

    return watchlist_item


def remove_movie_from_watchlist(*, user, movie_id):
    deleted_count, _ = Watchlist.objects.filter(
        user=user,
        movie_id=movie_id,
    ).delete()

    if deleted_count == 0:
        raise WatchlistItemNotFound()

    return deleted_count


def movie_in_watchlist(*, user, movie_id):
    return Watchlist.objects.filter(
        user=user,
        movie_id=movie_id,
    ).exists()


def user_watchlist(*, user):
    return Watchlist.objects.select_related("movie").filter(user=user)