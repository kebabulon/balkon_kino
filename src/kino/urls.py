from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kino.api.views import GenreViewSet, MovieViewSet, WatchlistViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"genres", GenreViewSet, basename="genre")
router.register(r"watchlist", WatchlistViewSet, basename="watchlist")

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
