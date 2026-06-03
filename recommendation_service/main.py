from fastapi import FastAPI
from .routers import auth, recommendations
from contextlib import asynccontextmanager
import asyncio
from .tasks import update_popular_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.popular_cache = []
    asyncio.create_task(periodic_cache_update(app))
    yield


async def periodic_cache_update(app: FastAPI):
    while True:
        await update_popular_cache(app.state)
        await asyncio.sleep(60)

app = FastAPI(title="Recommendation Service", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(recommendations.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
