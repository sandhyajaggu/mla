from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.crud.crud_achievement import achievement as crud_achievement
from app.models.admin_user import AdminUser
from app.schemas.achievement import AchievementCreate, AchievementOut, AchievementUpdate

router = APIRouter()


@router.get("", response_model=list[AchievementOut])
def list_achievements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Public — Achievements.js / Accomplishments.js / Excllence.js."""
    return crud_achievement.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=AchievementOut, status_code=status.HTTP_201_CREATED)
def create_achievement(
    payload: AchievementCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    return crud_achievement.create(db, obj_in=payload.model_dump())


@router.put("/{item_id}", response_model=AchievementOut)
def update_achievement(
    item_id: int,
    payload: AchievementUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    obj = crud_achievement.get(db, item_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Achievement not found")
    return crud_achievement.update(db, db_obj=obj, obj_in=payload.model_dump(exclude_unset=True))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_achievement(
    item_id: int, db: Session = Depends(get_db), _: AdminUser = Depends(get_current_admin)
):
    obj = crud_achievement.remove(db, id=item_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Achievement not found")
