"""
Maps to BeneficiariesForm.jsx / BeneficiariesTable.js (the "Schemes" module,
which also covers the Super Six schemes as category values rather than
separate tables).
"""
import enum

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin


class SchemeCategory(str, enum.Enum):
    welfare = "welfare"
    women = "women"
    education = "education"
    health = "health"
    agriculture = "agriculture"
    employment = "employment"
    housing = "housing"
    transport = "transport"
    pension = "pension"
    youth = "youth"
    scstbc = "scstbc"
    minority = "minority"
    finance = "finance"
    digital = "digital"
    infrastructure = "infrastructure"
    environment = "environment"
    rural = "rural"
    urban = "urban"
    women_child = "women-child"
    other = "other"


class SchemeStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class Scheme(Base, TimestampMixin):
    __tablename__ = "schemes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_description: Mapped[str] = mapped_column(String(500), nullable=False)
    badge_text: Mapped[str] = mapped_column(String(100), nullable=False)
    detailed_description: Mapped[str] = mapped_column(Text, nullable=False)
    thumbnail_url: Mapped[str] = mapped_column(String(500), nullable=False)
    beneficiaries: Mapped[str] = mapped_column(String(255), nullable=False)
    service_provider: Mapped[str] = mapped_column(String(255), nullable=False)
    launch_date: Mapped[Date] = mapped_column(Date, nullable=False)
    category: Mapped[SchemeCategory] = mapped_column(Enum(SchemeCategory), nullable=False)
    status: Mapped[SchemeStatus] = mapped_column(Enum(SchemeStatus), default=SchemeStatus.active)

    gallery_images: Mapped[list["SchemeImage"]] = relationship(
        back_populates="scheme", cascade="all, delete-orphan"
    )


class SchemeImage(Base):
    __tablename__ = "scheme_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scheme_id: Mapped[int] = mapped_column(Integer, ForeignKey("schemes.id"))
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)

    scheme: Mapped["Scheme"] = relationship(back_populates="gallery_images")
