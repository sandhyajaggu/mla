from app.crud.base import CRUDBase
from app.models.gallery_item import GalleryItem
from app.schemas.gallery_item import GalleryItemCreate, GalleryItemUpdate

gallery = CRUDBase[GalleryItem, GalleryItemCreate, GalleryItemUpdate](GalleryItem)
