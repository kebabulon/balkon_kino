from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from kino.domain.errors import (
    WatchlistAlreadyContainsMovie,
    WatchlistItemNotFound,
)
from kino.models import Genre, Movie, Watchlist
from kino.services.watchlist import (
    add_movie_to_watchlist,
    movie_in_watchlist,
    remove_movie_from_watchlist,
)


User = get_user_model()


class WatchlistServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="secret12345",
        )
        self.genre = Genre.objects.create(
            name="Drama",
            description="Drama genre",
        )
        self.movie = Movie.objects.create(
            title="Example Movie",
            description="Example description",
            release_date=2024,
            maturity_rating="PG",
            runtime=timedelta(hours=2),
        )
        self.movie.genres.add(self.genre)

    def test_add_movie_to_watchlist_creates_item(self):
        watchlist_item = add_movie_to_watchlist(user=self.user, movie=self.movie)

        self.assertEqual(watchlist_item.user, self.user)
        self.assertEqual(watchlist_item.movie, self.movie)
        self.assertTrue(movie_in_watchlist(user=self.user, movie_id=self.movie.id))

    def test_add_movie_to_watchlist_rejects_duplicates(self):
        add_movie_to_watchlist(user=self.user, movie=self.movie)

        with self.assertRaises(WatchlistAlreadyContainsMovie):
            add_movie_to_watchlist(user=self.user, movie=self.movie)

        self.assertEqual(Watchlist.objects.count(), 1)

    def test_remove_movie_from_watchlist_deletes_item(self):
        add_movie_to_watchlist(user=self.user, movie=self.movie)

        removed_count = remove_movie_from_watchlist(user=self.user, movie_id=self.movie.id)

        self.assertEqual(removed_count, 1)
        self.assertFalse(movie_in_watchlist(user=self.user, movie_id=self.movie.id))

    def test_remove_movie_from_watchlist_raises_for_missing_item(self):
        with self.assertRaises(WatchlistItemNotFound):
            remove_movie_from_watchlist(user=self.user, movie_id=self.movie.id)
