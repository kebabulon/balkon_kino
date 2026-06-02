from fastapi import Request, HTTPException, status, Depends
from typing import Optional
from .auth import decode_token


async def get_token_from_cookie(request: Request) -> Optional[str]:
    cookie_value = request.cookies.get("access_token")
    if not cookie_value:
        return None
    if cookie_value.startswith("Bearer "):
        return cookie_value[7:]
    return cookie_value


async def get_current_user_id(token: Optional[str] = Depends(get_token_from_cookie)) -> int:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (cookie missing)"
        )
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user_id in token"
        )
    return int(user_id)
