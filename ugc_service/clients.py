import requests
from flask import current_app

from .exceptions import ServiceUnavailableError

def check_movie_exists(movie_id: int) -> bool:
    base_url = current_app.config["DJANGO_API_BASE_URL"].rstrip("/")
    url = f"{base_url}/movies/{movie_id}/"
    try:
        response = requests.get(url, timeout=2.0)
    except requests.RequestException:
        raise ServiceUnavailableError("Не удалось проверить связанный объект в Django API")

    if response.status_code == 200:
        return True
    if response.status_code == 404:
        return False

    raise ServiceUnavailableError("Django API вернул неожиданный ответ")
