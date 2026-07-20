from pydantic import BaseModel, ConfigDict


class VoterStatBase(BaseModel):
    icon: str
    tone: str
    title: str
    value: str
    description: str
    display_order: int = 0


class VoterStatCreate(VoterStatBase):
    pass


class VoterStatUpdate(BaseModel):
    icon: str | None = None
    tone: str | None = None
    title: str | None = None
    value: str | None = None
    description: str | None = None
    display_order: int | None = None


class VoterStatOut(VoterStatBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ConstituencyInfoBase(BaseModel):
    label: str
    value: str
    link: str | None = None
    display_order: int = 0


class ConstituencyInfoCreate(ConstituencyInfoBase):
    pass


class ConstituencyInfoUpdate(BaseModel):
    label: str | None = None
    value: str | None = None
    link: str | None = None
    display_order: int | None = None


class ConstituencyInfoOut(ConstituencyInfoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
