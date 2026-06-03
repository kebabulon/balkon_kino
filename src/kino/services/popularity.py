from django.db.models import Count
from kino.models import Watchlist


def get_popular_movies(limit: int = 10):
    return list(Watchlist.objects.values('movie_id', 'movie__title')
                .annotate(count=Count('movie_id'))
                .order_by('-count')[:limit])
