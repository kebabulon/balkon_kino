from __future__ import annotations

from django.http import Http404
from rest_framework.exceptions import APIException, ErrorDetail, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from kino.domain.errors import DomainError


def _normalize_detail(detail):
    if isinstance(detail, dict):
        return {key: _normalize_detail(value) for key, value in detail.items()}
    if isinstance(detail, list):
        return [_normalize_detail(value) for value in detail]
    if isinstance(detail, ErrorDetail):
        return str(detail)
    return detail


def _error_response(detail, code, status_code):
    return Response(
        {"errors": [{"code": code, "detail": _normalize_detail(detail)}]},
        status=status_code,
    )


def api_exception_handler(exc, context):
    if isinstance(exc, DomainError):
        return _error_response(exc.detail, exc.code, exc.status_code)

    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(exc, ValidationError):
        code = "validation_error"
    elif isinstance(exc, Http404):
        code = "not_found"
    elif isinstance(exc, APIException):
        code = getattr(exc, "default_code", "error")
    else:
        code = "error"

    detail = response.data
    if isinstance(detail, dict) and set(detail.keys()) == {"detail"}:
        detail = detail["detail"]

    return _error_response(detail, code, response.status_code)