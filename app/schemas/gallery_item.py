from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.gallery_item import GalleryCategory


class GalleryItemBase(BaseModel):
    title: str
    category: GalleryCategory
    image_url: str | None = None
    video_url: str | None = None
    event_date: date | None = None


class GalleryItemCreate(GalleryItemBase):
    pass


class GalleryItemUpdate(BaseModel):
    title: str | None = None
    category: GalleryCategory | None = None
    image_url: str | None = None
    video_url: str | None = None
    event_date: date | None = None


class GalleryItemOut(GalleryItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
