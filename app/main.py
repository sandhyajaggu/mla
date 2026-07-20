"""
FastAPI application entrypoint.
Run locally with: uvicorn app.main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serves uploaded images/videos/audio at http://.../media/<subdir>/<file>
app.mount("/media", StaticFiles(directory=settings.MEDIA_ROOT), name="media")

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}
