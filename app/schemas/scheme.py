from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.scheme import SchemeCategory, SchemeStatus


class SchemeImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_url: str


class SchemeBase(BaseModel):
    name: str
    short_description: str
    badge_text: str
    detailed_description: str
    thumbnail_url: str
    beneficiaries: str
    service_provider: str
    launch_date: date
    category: SchemeCategory
    status: SchemeStatus = SchemeStatus.active


class SchemeCreate(SchemeBase):
    gallery_image_urls: list[str] = []


class SchemeUpdate(BaseModel):
    name: str | None = None
    short_description: str | None = None
    badge_text: str | None = None
    detailed_description: str | None = None
    thumbnail_url: str | None = None
    beneficiaries: str | None = None
    service_provider: str | None = None
    launch_date: date | None = None
    category: SchemeCategory | None = None
    status: SchemeStatus | None = None


class SchemeOut(SchemeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    gallery_images: list[SchemeImageOut] = []
