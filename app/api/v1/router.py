"""
Aggregates every endpoint router under one api_router, which app/main.py
mounts under settings.API_V1_PREFIX (/api/v1). Add new modules here.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    achievements,
    auth,
    cmrf,
    contact,
    development,
    gallery,
    media,
    schemes,
    uploads,
    voters,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(schemes.router, prefix="/schemes", tags=["schemes"])
api_router.include_router(cmrf.router, prefix="/cmrf", tags=["cmrf"])
api_router.include_router(development.router, prefix="/development", tags=["development"])
api_router.include_router(media.router, prefix="/media-items", tags=["media"])
api_router.include_router(gallery.router, prefix="/gallery", tags=["gallery"])
api_router.include_router(achievements.router, prefix="/achievements", tags=["achievements"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(voters.router, prefix="/voters", tags=["voters"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
