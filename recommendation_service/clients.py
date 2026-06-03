import httpx
from fastapi import HTTPException
from .config import settings


async def verify_user_credentials(username: str, password: str) -> dict | None:
    url = f"{settings.DJANGO_API_BASE_URL}/users/verify/"
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.post(url, json={"username": username, "password": password})
            if response.status_code == 200:
                return response.json()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Django API timeout")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Django API unavailable")
    return None


async def get_popular_movies_from_django() -> list:
    url = f"{settings.DJANGO_API_BASE_URL}/popular-movies/"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and "results" in data:
                    return data["results"]
                return data if isinstance(data, list) else []
        except Exception:
            pass
    return []


async def get_movies_by_genre(genre_name: str) -> list[dict]:
    url = f"{settings.DJANGO_API_BASE_URL}/movies/by_genre/?genre={genre_name}"
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            return resp.json().get('results', [])
    return []


async def get_user_watchlist_with_genres(user_id: int) -> list[dict]:
    url = f"{settings.DJANGO_API_BASE_URL}/watchlist/by_user/?user_id={user_id}"
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
    return []
