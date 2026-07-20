"""
Handles validating and saving uploaded files (images/video/audio) to disk
and returning a URL the frontend can use. Swap this module's internals for
an S3/Cloud Storage client later without touching any endpoint code.
"""
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}
ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/mp3", "audio/wav"}

KIND_CONFIG = {
    "image": (ALLOWED_IMAGE_TYPES, settings.MAX_IMAGE_SIZE_MB, "images"),
    "video": (ALLOWED_VIDEO_TYPES, settings.MAX_VIDEO_SIZE_MB, "videos"),
    "audio": (ALLOWED_AUDIO_TYPES, settings.MAX_AUDIO_SIZE_MB, "audio"),
}


def save_upload(file: UploadFile, kind: str) -> str:
    """Validate + persist an uploaded file. Returns a relative URL path."""
    if kind not in KIND_CONFIG:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid upload kind")

    allowed_types, max_mb, subdir = KIND_CONFIG[kind]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type for {kind}: {file.content_type}",
        )

    contents = file.file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > max_mb:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"File too large ({size_mb:.1f}MB) — max {max_mb}MB for {kind}",
        )

    ext = Path(file.filename or "").suffix
    unique_name = f"{uuid.uuid4().hex}{ext}"

    target_dir = Path(settings.MEDIA_ROOT) / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / unique_name

    with open(target_path, "wb") as f:
        f.write(contents)

    return f"/media/{subdir}/{unique_name}"


def delete_upload(url: str) -> None:
    """Best-effort delete of a previously-saved file given its /media/... URL."""
    if not url.startswith("/media/"):
        return
    path = Path(settings.MEDIA_ROOT) / url.removeprefix("/media/")
    path.unlink(missing_ok=True)
