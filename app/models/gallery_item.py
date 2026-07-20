"""Maps to src/components/gallery/*.js (Photos, Events, Press, Leaders,
Sports, Spiritual, Inaugurations, Others, Videos)."""
import enum

from sqlalchemy import Date, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin


class GalleryCategory(str, enum.Enum):
    photos = "photos"
    videos = "videos"
    events = "events"
    press = "press"
    leaders = "leaders"
    sports = "sports"
    spiritual = "spiritual"
    inaugurations = "inaugurations"
    others = "others"


class GalleryItem(Base, TimestampMixin):
    __tablename__ = "gallery_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[GalleryCategory] = mapped_column(Enum(GalleryCategory), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    event_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
