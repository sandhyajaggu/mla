"""Maps to DevelopmentForm.js / Development.js"""
import enum

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin


class DevMandal(str, enum.Enum):
    kandukur = "Kandukur"
    lingasamudram = "Lingasamudram"
    gudluru = "Gudluru"
    ulavapadu = "Ulavapadu"
    voletivaripalem = "Voletivaripalem"


class DevCategory(str, enum.Enum):
    road_works = "Road Works"
    water_supply = "Water Supply"
    drainage = "Drainage"


class DevelopmentWork(Base, TimestampMixin):
    __tablename__ = "development_works"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mandal: Mapped[DevMandal] = mapped_column(Enum(DevMandal), nullable=False)
    category: Mapped[DevCategory] = mapped_column(Enum(DevCategory), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    estimated_cost: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    images: Mapped[list["DevelopmentImage"]] = relationship(
        back_populates="development_work", cascade="all, delete-orphan"
    )


class DevelopmentImage(Base):
    __tablename__ = "development_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    development_work_id: Mapped[int] = mapped_column(Integer, ForeignKey("development_works.id"))
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)

    development_work: Mapped["DevelopmentWork"] = relationship(back_populates="images")
