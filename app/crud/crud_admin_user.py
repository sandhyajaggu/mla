from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.admin_user import AdminUser


def get_by_email(db: Session, *, email: str) -> AdminUser | None:
    return db.query(AdminUser).filter(AdminUser.email == email).first()


def authenticate(db: Session, *, email: str, password: str) -> AdminUser | None:
    user = get_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_admin(db: Session, *, email: str, password: str, full_name: str | None = None) -> AdminUser:
    db_obj = AdminUser(email=email, hashed_password=hash_password(password), full_name=full_name)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
