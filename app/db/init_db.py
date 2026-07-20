"""
One-time script to create the first admin user, so you're not stuck with
the frontend's hardcoded admin@gmail.com / admin123 dummy login.

Run after migrations are applied:
    python -m app.db.init_db
"""
from app.core.config import settings
from app.crud.crud_admin_user import create_admin, get_by_email
from app.db.session import SessionLocal


def init_first_admin() -> None:
    db = SessionLocal()
    try:
        existing = get_by_email(db, email=settings.FIRST_ADMIN_EMAIL)
        if existing:
            print(f"Admin already exists: {settings.FIRST_ADMIN_EMAIL}")
            return
        create_admin(
            db,
            email=settings.FIRST_ADMIN_EMAIL,
            password=settings.FIRST_ADMIN_PASSWORD,
            full_name="Portal Admin",
        )
        print(f"Created first admin: {settings.FIRST_ADMIN_EMAIL}")
    finally:
        db.close()


if __name__ == "__main__":
    init_first_admin()
