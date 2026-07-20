"""Maps to Voters.js — the stat cards and constituency info are currently
hardcoded in the frontend; these two tables make them admin-editable."""
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin


class VoterStat(Base, TimestampMixin):
    """One row per stat card, e.g. 'Total Voters' -> '2,18,859'."""
    __tablename__ = "voter_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon: Mapped[str] = mapped_column(String(50), nullable=False)   # e.g. "users", "pie"
    tone: Mapped[str] = mapped_column(String(50), nullable=False)   # e.g. "indigo", "green"
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)


class ConstituencyInfo(Base, TimestampMixin):
    """One row per info line, e.g. 'District' -> 'Prakasam'."""
    __tablename__ = "constituency_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
