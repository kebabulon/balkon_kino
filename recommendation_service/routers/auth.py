from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from ..auth import create_access_token
from ..clients import verify_user_credentials
from ..config import settings


class UserLogin(BaseModel):
    username: str
    password: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(user: UserLogin, response: Response):
    user_data = await verify_user_credentials(user.username, user.password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=user_data["id"], is_user=True)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=False,          # True в production с HTTPS
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"message": "Logged in successfully"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
