from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]


def get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_list(name: str, default: list[str] | None = None) -> list[str]:
    value = os.getenv(name)
    if value is None or not value.strip():
        return list(default or [])

    return [item.strip() for item in value.split(",") if item.strip()]


SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-*l_zafys4y(y%=o=fkrr!rslclpc!qoh-h=0+p5@jb6xdh=b#l",
)
DEBUG = get_bool("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = get_list("DJANGO_ALLOWED_HOSTS", default=[])