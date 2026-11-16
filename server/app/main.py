from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db, AsyncSessionLocal
from .seed import seed_database
from .routers import auth, settings as settings_router, resources


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with AsyncSessionLocal() as db:
        await seed_database(db)
    yield


app = FastAPI(title="rgzn-ai API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["健康检查"])
async def health():
    return {"code": 0, "message": "ok", "data": {"status": "healthy"}}


app.include_router(auth.router)
app.include_router(settings_router.router)
app.include_router(resources.router)
