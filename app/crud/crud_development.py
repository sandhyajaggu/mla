from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.development_work import DevelopmentImage, DevelopmentWork
from app.schemas.development_work import DevelopmentWorkCreate, DevelopmentWorkUpdate


class CRUDDevelopment(CRUDBase[DevelopmentWork, DevelopmentWorkCreate, DevelopmentWorkUpdate]):
    def create_with_images(self, db: Session, *, obj_in: DevelopmentWorkCreate) -> DevelopmentWork:
        data = obj_in.model_dump(exclude={"image_urls"})
        db_obj = DevelopmentWork(**data)
        db_obj.images = [DevelopmentImage(image_url=url) for url in obj_in.image_urls]
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


development = CRUDDevelopment(DevelopmentWork)
