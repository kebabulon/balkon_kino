from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters

from kino.permissions import IsAdminUserOrReadOnly

from kino.models import Movie, Genre, Watchlist
from kino.serializers import MovieSerializer, GenreSerializer


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
