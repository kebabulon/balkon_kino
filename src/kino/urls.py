from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kino import views

router = DefaultRouter()
router.register(r"movies", views.MovieViewSet, basename="movie")
router.register(r"genres", views.GenreViewSet, basename="genre")
router.register(r"watchlist", views.WatchlistViewSet, basename="watchlist")

urlpatterns = [
    path("", include(router.urls)),
]
