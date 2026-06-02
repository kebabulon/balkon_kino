from fastapi import FastAPI, Depends
from .routers import auth, recommendations
from .dependencies import get_current_user_id

app = FastAPI(title="Recommendation Service")

app.include_router(auth.router)
app.include_router(recommendations.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
