from django.contrib import admin

from kino.models import Movie, Genre, Watchlist, Subscription


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


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "subscription_plan",
        "expiration_date",
        "is_valid",
    )
    list_filter = (
        "subscription_plan",
        "expiration_date",
    )
    search_fields = (
        "user",
    )
    ordering = ("-expiration_date",)
    readonly_fields = ("is_valid",)

    def is_valid(self, subscription):
        from django.utils import timezone
        return subscription.expiration_date > timezone.now()
    is_valid.boolean = True
