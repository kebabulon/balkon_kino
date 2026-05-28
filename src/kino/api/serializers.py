from rest_framework import serializers

from kino.models import Genre, Movie, Watchlist


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ["url", "id", "name", "description"]


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Genre.objects.all(),
    )

    class Meta:
        model = Movie
        fields = [
            "url",
            "id",
            "title",
            "description",
            "release_date",
            "maturity_rating",
            "runtime",
            "genres",
        ]


class WatchlistSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Watchlist
        fields = [
            "user",
            "movie",
            "created_at",
        ]


class WatchlistCheckSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField(min_value=1)