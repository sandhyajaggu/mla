from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.scheme import Scheme, SchemeCategory, SchemeImage, SchemeStatus
from app.schemas.scheme import SchemeCreate, SchemeUpdate


class CRUDScheme(CRUDBase[Scheme, SchemeCreate, SchemeUpdate]):
    def create_with_images(self, db: Session, *, obj_in: SchemeCreate) -> Scheme:
        data = obj_in.model_dump(exclude={"gallery_image_urls"})
        db_obj = Scheme(**data)
        db_obj.gallery_images = [SchemeImage(image_url=url) for url in obj_in.gallery_image_urls]
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_filtered(
        self,
        db: Session,
        *,
        category: SchemeCategory | None = None,
        status: SchemeStatus | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Scheme]:
        query = db.query(Scheme)
        if category:
            query = query.filter(Scheme.category == category)
        if status:
            query = query.filter(Scheme.status == status)
        return query.offset(skip).limit(limit).all()


scheme = CRUDScheme(Scheme)
