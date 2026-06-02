from fastapi import APIRouter, Depends
from ..dependencies import get_current_user_id

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/for-user")
async def personal_recommendations(user_id: int = Depends(get_current_user_id)):
    return {"message": f"User {user_id} recommendations"}
