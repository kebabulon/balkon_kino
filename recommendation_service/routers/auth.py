from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from ..auth import verify_password, get_password_hash, create_access_token
from ..config import settings

fake_users_db = {}


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(400, "Username already exists")
    hashed = get_password_hash(user.password)
    user_id = len(fake_users_db) + 1
    fake_users_db[user.username] = {
        "id": user_id,
        "username": user.username,
        "password": hashed
    }
    return {"message": "User created successfully"}


@router.post("/login")
async def login(user: UserLogin, response: Response):
    db_user = fake_users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(subject=db_user["id"], is_user=True)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"message": "Logged in successfully"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
