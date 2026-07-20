from datetime import date as dt_date
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.cmrf_beneficiary import CmrfStatus, Mandal


class CmrfBeneficiaryBase(BaseModel):
    name: str
    relation: str
    amount: Decimal
    village: str
    mandal: Mandal
    date: dt_date
    mobile: str = Field(min_length=10, max_length=15)
    status: CmrfStatus = CmrfStatus.pending
    remarks: str | None = None
    image_url: str | None = None
    video_url: str | None = None


class CmrfBeneficiaryCreate(CmrfBeneficiaryBase):
    # Full Aadhaar accepted on input only, never stored or returned in full.
    aadhaar: str = Field(min_length=12, max_length=12)


class CmrfBeneficiaryUpdate(BaseModel):
    name: str | None = None
    relation: str | None = None
    amount: Decimal | None = None
    village: str | None = None
    mandal: Mandal | None = None
    date: dt_date | None = None
    mobile: str | None = None
    status: CmrfStatus | None = None
    remarks: str | None = None
    image_url: str | None = None
    video_url: str | None = None


class CmrfBeneficiaryOut(CmrfBeneficiaryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    aadhaar_last4: str
    created_at: datetime
