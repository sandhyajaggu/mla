from app.crud.base import CRUDBase
from app.models.voter_stat import ConstituencyInfo, VoterStat
from app.schemas.voter_stat import (
    ConstituencyInfoCreate,
    ConstituencyInfoUpdate,
    VoterStatCreate,
    VoterStatUpdate,
)

voter_stat = CRUDBase[VoterStat, VoterStatCreate, VoterStatUpdate](VoterStat)
constituency_info = CRUDBase[ConstituencyInfo, ConstituencyInfoCreate, ConstituencyInfoUpdate](
    ConstituencyInfo
)
