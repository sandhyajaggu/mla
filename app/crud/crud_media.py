from app.crud.base import CRUDBase
from app.models.media import MediaItem
from app.schemas.media import MediaItemCreate, MediaItemUpdate

media = CRUDBase[MediaItem, MediaItemCreate, MediaItemUpdate](MediaItem)
