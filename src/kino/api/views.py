from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kino.api.serializers import (
    GenreSerializer,
    MovieSerializer,
    WatchlistCheckSerializer,
    WatchlistSerializer,
)
from kino.models import Genre, Movie
from kino.permissions import IsAdminUserOrReadOnly
from kino.services.watchlist import (
    add_movie_to_watchlist,
    movie_in_watchlist,
    remove_movie_from_watchlist,
    user_watchlist,
)


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "release_date"]

    def get_queryset(self):
        queryset = Movie.objects.all()
        maturity_rating = self.request.query_params.get("maturity_rating")
        if maturity_rating:
            queryset = queryset.filter(maturity_rating=maturity_rating)
        release_date = self.request.query_params.get("release_date")
        if release_date:
            queryset = queryset.filter(release_date=release_date)
        return queryset


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return user_watchlist(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        watchlist_item = add_movie_to_watchlist(
            user=request.user,
            movie=serializer.validated_data["movie"],
        )
        output_serializer = self.get_serializer(watchlist_item)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        remove_movie_from_watchlist(
            user=request.user,
            movie_id=kwargs.get("pk"),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def check(self, request):
        serializer = WatchlistCheckSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        exists = movie_in_watchlist(
            user=request.user,
            movie_id=serializer.validated_data["movie_id"],
        )
        return Response({"in_watchlist": exists})