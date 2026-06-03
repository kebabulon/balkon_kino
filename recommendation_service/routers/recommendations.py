from fastapi import APIRouter, Depends, HTTPException, Request
from collections import Counter
from ..dependencies import get_current_user_id
from ..clients import get_user_watchlist_with_genres, get_movies_by_genre

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/for-user")
async def personal_recommendations(user_id: int = Depends(get_current_user_id)):
    return {"message": f"User {user_id} recommendations"}


@router.get("/by-favorite-genre")
async def recommendations_by_favorite_genre(
    user_id: int = Depends(get_current_user_id),
    request: Request = None
):
    watchlist = await get_user_watchlist_with_genres(user_id)
    if not watchlist:
        raise HTTPException(404, "No watched movies found")
    genre_counter = Counter()
    for item in watchlist:
        for genre in item.get("genres", []):
            genre_counter[genre] += 1
    if not genre_counter:
        raise HTTPException(404, "No genre information")
    favorite_genre = genre_counter.most_common(1)[0][0]
    movies = await get_movies_by_genre(favorite_genre)
    return {
        "favorite_genre": favorite_genre,
        "recommendations": movies
    }


@router.get("/debug-cache")
async def debug_cache(request: Request):
    return {"cache": getattr(request.app.state, "popular_cache", [])}
