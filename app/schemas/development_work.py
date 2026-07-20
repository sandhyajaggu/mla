from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.development_work import DevCategory, DevMandal


class DevelopmentImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_url: str


class DevelopmentWorkBase(BaseModel):
    mandal: DevMandal
    category: DevCategory
    title: str
    estimated_cost: str | None = None
    description: str


class DevelopmentWorkCreate(DevelopmentWorkBase):
    image_urls: list[str] = []


class DevelopmentWorkUpdate(BaseModel):
    mandal: DevMandal | None = None
    category: DevCategory | None = None
    title: str | None = None
    estimated_cost: str | None = None
    description: str | None = None


class DevelopmentWorkOut(DevelopmentWorkBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    images: list[DevelopmentImageOut] = []
