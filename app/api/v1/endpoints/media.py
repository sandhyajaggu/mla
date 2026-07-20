from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.crud.crud_media import media as crud_media
from app.models.admin_user import AdminUser
from app.models.media import MediaType
from app.schemas.media import MediaItemCreate, MediaItemOut, MediaItemUpdate

router = APIRouter()


@router.get("", response_model=list[MediaItemOut])
def list_media(
    media_type: MediaType | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Public — backs both Mp3Table.js and Mp4Table.js (filter by ?media_type=audio|video)."""
    query = db.query(crud_media.model)
    if media_type:
        query = query.filter(crud_media.model.media_type == media_type)
    return query.offset(skip).limit(limit).all()


@router.post("", response_model=MediaItemOut, status_code=status.HTTP_201_CREATED)
def create_media(
    payload: MediaItemCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    """Admin only — Mp3Form.js / Mp4Form.js submit."""
    return crud_media.create(db, obj_in=payload.model_dump())


@router.put("/{media_id}", response_model=MediaItemOut)
def update_media(
    media_id: int,
    payload: MediaItemUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    obj = crud_media.get(db, media_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Media item not found")
    return crud_media.update(db, db_obj=obj, obj_in=payload.model_dump(exclude_unset=True))


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_media(
    media_id: int, db: Session = Depends(get_db), _: AdminUser = Depends(get_current_admin)
):
    obj = crud_media.remove(db, id=media_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Media item not found")
