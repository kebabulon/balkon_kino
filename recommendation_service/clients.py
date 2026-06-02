import httpx
from fastapi import HTTPException
from .config import settings


async def verify_user_credentials(username: str, password: str) -> dict | None:
    """Асинхронно проверяет пользователя через Django (аналог Flask-вызова)"""
    url = f"{settings.DJANGO_API_BASE_URL}/verify-user/"
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
