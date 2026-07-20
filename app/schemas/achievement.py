from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class AchievementBase(BaseModel):
    title: str
    description: str
    image_url: str | None = None
    achieved_on: date | None = None


class AchievementCreate(AchievementBase):
    pass


class AchievementUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    achieved_on: date | None = None


class AchievementOut(AchievementBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
