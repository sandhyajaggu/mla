from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.crud.crud_scheme import scheme as crud_scheme
from app.models.admin_user import AdminUser
from app.models.scheme import SchemeCategory, SchemeStatus
from app.schemas.scheme import SchemeCreate, SchemeOut, SchemeUpdate

router = APIRouter()


@router.get("", response_model=list[SchemeOut])
def list_schemes(
    category: SchemeCategory | None = None,
    status_filter: SchemeStatus | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Public — powers the schemes listing page."""
    return crud_scheme.get_filtered(db, category=category, status=status_filter, skip=skip, limit=limit)


@router.get("/{scheme_id}", response_model=SchemeOut)
def get_scheme(scheme_id: int, db: Session = Depends(get_db)):
    """Public — scheme detail page."""
    obj = crud_scheme.get(db, scheme_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Scheme not found")
    return obj


@router.post("", response_model=SchemeOut, status_code=status.HTTP_201_CREATED)
def create_scheme(
    payload: SchemeCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    """Admin only — BeneficiariesForm.jsx submit."""
    return crud_scheme.create_with_images(db, obj_in=payload)


@router.put("/{scheme_id}", response_model=SchemeOut)
def update_scheme(
    scheme_id: int,
    payload: SchemeUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    obj = crud_scheme.get(db, scheme_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Scheme not found")
    return crud_scheme.update(db, db_obj=obj, obj_in=payload.model_dump(exclude_unset=True))


@router.delete("/{scheme_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scheme(
    scheme_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    obj = crud_scheme.remove(db, id=scheme_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Scheme not found")
