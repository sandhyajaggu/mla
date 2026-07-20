from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.crud.crud_gallery import gallery as crud_gallery
from app.models.admin_user import AdminUser
from app.models.gallery_item import GalleryCategory
from app.schemas.gallery_item import GalleryItemCreate, GalleryItemOut, GalleryItemUpdate

router = APIRouter()


@router.get("", response_model=list[GalleryItemOut])
def list_gallery(
    category: GalleryCategory | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Public — backs every gallery/*.js page via ?category=photos|events|press|..."""
    query = db.query(crud_gallery.model)
    if category:
        query = query.filter(crud_gallery.model.category == category)
    return query.offset(skip).limit(limit).all()


@router.post("", response_model=GalleryItemOut, status_code=status.HTTP_201_CREATED)
def create_gallery_item(
    payload: GalleryItemCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    return crud_gallery.create(db, obj_in=payload.model_dump())


@router.put("/{item_id}", response_model=GalleryItemOut)
def update_gallery_item(
    item_id: int,
    payload: GalleryItemUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    obj = crud_gallery.get(db, item_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Gallery item not found")
    return crud_gallery.update(db, db_obj=obj, obj_in=payload.model_dump(exclude_unset=True))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gallery_item(
    item_id: int, db: Session = Depends(get_db), _: AdminUser = Depends(get_current_admin)
):
    obj = crud_gallery.remove(db, id=item_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Gallery item not found")
