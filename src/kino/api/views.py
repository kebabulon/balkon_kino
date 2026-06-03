from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import authenticate
from django.db.models import Count

from kino.api.serializers import (
    GenreSerializer,
    MovieSerializer,
    WatchlistCheckSerializer,
    WatchlistSerializer,
    PopularitySerializer,
)
from kino.models import Genre, Movie, Watchlist
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

    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        genre = request.query_params.get('genre')
        if not genre:
            return Response({"error": "genre param required"}, status=400)
        movies = Movie.objects.filter(genres__name__iexact=genre)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)


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

    @action(detail=False, methods=['get'], url_path='by-user')
    def by_user(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id required"}, status=400)
        watchlist_items = Watchlist.objects.filter(user_id=user_id).select_related('movie')
        data = []
        for item in watchlist_items:
            movie = item.movie
            data.append({
                'id': movie.id,
                'title': movie.title,
                'genres': list(movie.genres.values_list('name', flat=True)),
                'added_at': item.created_at
            })
        return Response(data)


class UserViewSet(GenericViewSet):
    permission_classes = []

    @action(detail=False, methods=['post'], url_path='verify')
    def verify(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'id': user.id, 'username': user.username})
        return Response({'error': 'Invalid credentials'}, status=401)


class PopularMoviesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PopularitySerializer

    def get_queryset(self):
        return Watchlist.objects.values('movie_id', 'movie__title') \
            .annotate(count=Count('movie_id')) \
            .order_by('-count')[:5]
