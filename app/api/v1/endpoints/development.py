from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.crud.crud_development import development as crud_dev
from app.models.admin_user import AdminUser
from app.schemas.development_work import DevelopmentWorkCreate, DevelopmentWorkOut, DevelopmentWorkUpdate

router = APIRouter()


@router.get("", response_model=list[DevelopmentWorkOut])
def list_development(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Public — Development.js listing."""
    return crud_dev.get_multi(db, skip=skip, limit=limit)


@router.get("/{dev_id}", response_model=DevelopmentWorkOut)
def get_development(dev_id: int, db: Session = Depends(get_db)):
    obj = crud_dev.get(db, dev_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Development work not found")
    return obj


@router.post("", response_model=DevelopmentWorkOut, status_code=status.HTTP_201_CREATED)
def create_development(
    payload: DevelopmentWorkCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    return crud_dev.create_with_images(db, obj_in=payload)


@router.put("/{dev_id}", response_model=DevelopmentWorkOut)
def update_development(
    dev_id: int,
    payload: DevelopmentWorkUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    obj = crud_dev.get(db, dev_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Development work not found")
    return crud_dev.update(db, db_obj=obj, obj_in=payload.model_dump(exclude_unset=True))


@router.delete("/{dev_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_development(
    dev_id: int, db: Session = Depends(get_db), _: AdminUser = Depends(get_current_admin)
):
    obj = crud_dev.remove(db, id=dev_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Development work not found")
