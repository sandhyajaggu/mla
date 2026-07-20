from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.media import MediaType


class MediaItemBase(BaseModel):
    media_type: MediaType
    title: str
    description: str | None = None
    source_url: str


class MediaItemCreate(MediaItemBase):
    pass


class MediaItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    source_url: str | None = None


class MediaItemOut(MediaItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
