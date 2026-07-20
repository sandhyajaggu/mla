from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.crud.crud_voter import constituency_info as crud_info
from app.crud.crud_voter import voter_stat as crud_stat
from app.models.admin_user import AdminUser
from app.schemas.voter_stat import (
    ConstituencyInfoCreate,
    ConstituencyInfoOut,
    ConstituencyInfoUpdate,
    VoterStatCreate,
    VoterStatOut,
    VoterStatUpdate,
)

router = APIRouter()


# ---- Stat cards (Total Voters, Turnout, Male/Female, etc.) ----

@router.get("/stats", response_model=list[VoterStatOut])
def list_voter_stats(db: Session = Depends(get_db)):
    """Public — Voters.js stat cards."""
    return db.query(crud_stat.model).order_by(crud_stat.model.display_order).all()


@router.post("/stats", response_model=VoterStatOut, status_code=status.HTTP_201_CREATED)
def create_voter_stat(
    payload: VoterStatCreate, db: Session = Depends(get_db), _: AdminUser = Depends(get_current_admin)
):
    return crud_stat.create(db, obj_in=payload.model_dump())


@router.put("/stats/{stat_id}", response_model=VoterStatOut)
def update_voter_stat(
    stat_id: int,
    payload: VoterStatUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    obj = crud_stat.get(db, stat_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Voter stat not found")
    return crud_stat.update(db, db_obj=obj, obj_in=payload.model_dump(exclude_unset=True))


@router.delete("/stats/{stat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_voter_stat(
    stat_id: int, db: Session = Depends(get_db), _: AdminUser = Depends(get_current_admin)
):
    obj = crud_stat.remove(db, id=stat_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Voter stat not found")


# ---- Constituency info rows (District, LS Constituency, current MLA, etc.) ----

@router.get("/constituency-info", response_model=list[ConstituencyInfoOut])
def list_constituency_info(db: Session = Depends(get_db)):
    """Public — Voters.js constituency info table."""
    return db.query(crud_info.model).order_by(crud_info.model.display_order).all()


@router.post("/constituency-info", response_model=ConstituencyInfoOut, status_code=status.HTTP_201_CREATED)
def create_constituency_info(
    payload: ConstituencyInfoCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    return crud_info.create(db, obj_in=payload.model_dump())


@router.put("/constituency-info/{info_id}", response_model=ConstituencyInfoOut)
def update_constituency_info(
    info_id: int,
    payload: ConstituencyInfoUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    obj = crud_info.get(db, info_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Constituency info row not found")
    return crud_info.update(db, db_obj=obj, obj_in=payload.model_dump(exclude_unset=True))


@router.delete("/constituency-info/{info_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_constituency_info(
    info_id: int, db: Session = Depends(get_db), _: AdminUser = Depends(get_current_admin)
):
    obj = crud_info.remove(db, id=info_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Constituency info row not found")
