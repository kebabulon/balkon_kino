from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from kino.permissions import IsAdminUserOrReadOnly

from kino.models import Movie, Genre, Watchlist
from kino.serializers import MovieSerializer, GenreSerializer, WatchlistSerializer


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'release_date']

    def get_queryset(self):
        queryset = Movie.objects.all()
        maturity_rating = self.request.query_params.get('maturity_rating')
        if maturity_rating:
            queryset = queryset.filter(maturity_rating=maturity_rating)
        release_date = self.request.query_params.get('release_date')
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
        return Watchlist.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        movie_id = request.data.get("movie")
        if not movie_id:
            return Response(
                {"detail": "movie_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )
        movie = get_object_or_404(Movie, id=movie_id)
        watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)

        if not created:
            return Response(
                {"detail": "Фильм уже добавлен в Watchlist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(watchlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        movie_id = kwargs.get("pk")

        deleted = Watchlist.objects.filter(
            user=request.user,
            movie_id=movie_id,
        ).delete()

        if deleted[0] == 0:
            return Response(
                {"detail": "Фильма нет в избранном"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def check(self, request):
        movie_id = request.query_params.get("movie_id")
        if not movie_id:
            return Response(
                {"detail": "movie_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        exists = Watchlist.objects.filter(
            user=request.user,
            movie_id=movie_id
        ).exists()

        return Response({"in_watchlist": exists})
