from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.crud.crud_cmrf import cmrf as crud_cmrf
from app.models.admin_user import AdminUser
from app.schemas.cmrf_beneficiary import CmrfBeneficiaryCreate, CmrfBeneficiaryOut, CmrfBeneficiaryUpdate

router = APIRouter()


@router.get("", response_model=list[CmrfBeneficiaryOut])
def list_cmrf(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    """Admin only — CMRFTable.js. (CMRF records include PII, so unlike
    Schemes this whole resource is admin-only, not public.)"""
    return crud_cmrf.get_multi(db, skip=skip, limit=limit)


@router.get("/{cmrf_id}", response_model=CmrfBeneficiaryOut)
def get_cmrf(
    cmrf_id: int, db: Session = Depends(get_db), _: AdminUser = Depends(get_current_admin)
):
    obj = crud_cmrf.get(db, cmrf_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "CMRF record not found")
    return obj


@router.post("", response_model=CmrfBeneficiaryOut, status_code=status.HTTP_201_CREATED)
def create_cmrf(
    payload: CmrfBeneficiaryCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    return crud_cmrf.create_masked(db, obj_in=payload)


@router.put("/{cmrf_id}", response_model=CmrfBeneficiaryOut)
def update_cmrf(
    cmrf_id: int,
    payload: CmrfBeneficiaryUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    obj = crud_cmrf.get(db, cmrf_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "CMRF record not found")
    return crud_cmrf.update(db, db_obj=obj, obj_in=payload.model_dump(exclude_unset=True))


@router.delete("/{cmrf_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cmrf(
    cmrf_id: int, db: Session = Depends(get_db), _: AdminUser = Depends(get_current_admin)
):
    obj = crud_cmrf.remove(db, id=cmrf_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "CMRF record not found")
