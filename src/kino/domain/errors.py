from __future__ import annotations

from http import HTTPStatus


class DomainError(Exception):
    status_code = HTTPStatus.BAD_REQUEST
    code = "domain_error"
    default_detail = "Domain error"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class WatchlistMovieRequired(DomainError):
    status_code = HTTPStatus.BAD_REQUEST
    code = "movie_required"
    default_detail = "movie_id обязателен"


class MovieNotFound(DomainError):
    status_code = HTTPStatus.NOT_FOUND
    code = "movie_not_found"
    default_detail = "Фильм не найден"


class WatchlistAlreadyContainsMovie(DomainError):
    status_code = HTTPStatus.BAD_REQUEST
    code = "watchlist_exists"
    default_detail = "Фильм уже добавлен в Watchlist"


class WatchlistItemNotFound(DomainError):
    status_code = HTTPStatus.NOT_FOUND
    code = "watchlist_not_found"
    default_detail = "Фильма нет в избранном"