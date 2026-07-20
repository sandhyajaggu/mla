"""Maps to Mp3Form.js/Mp3Table.js and Mp4Form.js/Mp4Table.js — a single
table with a `media_type` discriminator, since both are just title +
description + a source (file for audio, YouTube URL for video)."""
import enum

from sqlalchemy import Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin


class MediaType(str, enum.Enum):
    audio = "audio"
    video = "video"


class MediaItem(Base, TimestampMixin):
    __tablename__ = "media_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    media_type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # for audio: uploaded file URL. for video: YouTube embed URL.
    source_url: Mapped[str] = mapped_column(String(500), nullable=False)
