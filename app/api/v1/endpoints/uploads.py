from fastapi import APIRouter, Depends, UploadFile

from app.api.deps import get_current_admin
from app.models.admin_user import AdminUser
from app.services.file_storage import save_upload

router = APIRouter()


@router.post("/{kind}")
def upload_file(kind: str, file: UploadFile, _: AdminUser = Depends(get_current_admin)):
    """
    Admin only. kind = 'image' | 'video' | 'audio'.
    Used by every dashboard form's file input (thumbnails, gallery images,
    development photos, CMRF video, MP3/MP4 uploads). Returns a URL to store
    on the parent record (e.g. Scheme.thumbnail_url, MediaItem.source_url).
    """
    url = save_upload(file, kind)
    return {"url": url}
