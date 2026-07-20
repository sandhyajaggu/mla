from app.crud.base import CRUDBase
from app.models.achievement import Achievement
from app.schemas.achievement import AchievementCreate, AchievementUpdate

achievement = CRUDBase[Achievement, AchievementCreate, AchievementUpdate](Achievement)
