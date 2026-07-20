from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    subject: str
    message: str


class ContactMessageUpdate(BaseModel):
    is_read: bool


class ContactMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    subject: str
    message: str
    is_read: bool
    created_at: datetime
