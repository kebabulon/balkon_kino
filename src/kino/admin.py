from django.contrib import admin

from kino.models import Movie, Genre, Watchlist


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "release_date",
        "maturity_rating",
        "runtime",
        "genre"
    )
    filter_horizontal = (
        'genres',
    )
    list_filter = (
        "maturity_rating",
        "release_date"
    )
    search_fields = (
        "title",
        "description"
    )
    ordering = ("title",)

    def genre(self, obj):
        return [genre.name for genre in obj.genres.all()]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
    )
    search_fields = (
        "name",
        "description"
    )
    ordering = ("name",)
