from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kino.api.views import GenreViewSet, MovieViewSet, WatchlistViewSet, UserViewSet, PopularMoviesViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"genres", GenreViewSet, basename="genre")
router.register(r"watchlist", WatchlistViewSet, basename="watchlist")
router.register(r'users', UserViewSet, basename='user')
router.register(r'popular-movies', PopularMoviesViewSet, basename='popular')

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
