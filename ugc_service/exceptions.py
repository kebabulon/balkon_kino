from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus


@dataclass(slots=True)
class APIError(Exception):
    status_code: int
    code: str
    detail: str | dict | list


class ValidationError(APIError):
    def __init__(self, detail: str | dict | list):
        super().__init__(HTTPStatus.BAD_REQUEST, "validation_error", detail)


class NotFoundError(APIError):
    def __init__(self, detail: str):
        super().__init__(HTTPStatus.NOT_FOUND, "not_found", detail)


class ServiceUnavailableError(APIError):
    def __init__(self, detail: str):
        super().__init__(HTTPStatus.SERVICE_UNAVAILABLE, "service_unavailable", detail)


class MovieNotFoundError(NotFoundError):
    def __init__(self, detail: str = "Связанный объект не найден"):
        super().__init__(detail)
        self.code = "linked_object_not_found"


class ReviewNotFoundError(NotFoundError):
    def __init__(self, detail: str = "UGC-объект не найден"):
        super().__init__(detail)
        self.code = "review_not_found"