"""Maps to CmrFundsForm.js / CMRFTable.js"""
import enum

from sqlalchemy import Date, Enum, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin


class Mandal(str, enum.Enum):
    kandukur = "Kandukur"
    gudluru = "Gudluru"
    ulavapadu = "Ulavapadu"
    lingasamudram = "Lingasamudram"
    voletivaripalem = "Voletivaripalem"


class CmrfStatus(str, enum.Enum):
    approved = "Approved"
    pending = "Pending"


class CmrfBeneficiary(Base, TimestampMixin):
    __tablename__ = "cmrf_beneficiaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    relation: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. S/O, W/O, D/O
    amount: Mapped[Numeric] = mapped_column(Numeric(12, 2), nullable=False)
    village: Mapped[str] = mapped_column(String(255), nullable=False)
    mandal: Mapped[Mandal] = mapped_column(Enum(Mandal), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    mobile: Mapped[str] = mapped_column(String(15), nullable=False)
    # Aadhaar is sensitive PII — store only the last 4 digits, never the full number.
    aadhaar_last4: Mapped[str] = mapped_column(String(4), nullable=False)
    status: Mapped[CmrfStatus] = mapped_column(Enum(CmrfStatus), default=CmrfStatus.pending)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
