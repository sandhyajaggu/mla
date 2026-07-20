from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.core.security import create_access_token
from app.crud.crud_admin_user import authenticate
from app.models.admin_user import AdminUser
from app.schemas.admin_user import AdminUserOut, Token

router = APIRouter()


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 password flow login. `form_data.username` is the admin's email.
    Swagger UI's "Authorize" button uses this endpoint automatically.
    """
    user = authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token(subject=user.email)
    return Token(access_token=token)


@router.get("/me", response_model=AdminUserOut)
def read_current_admin(current_admin: AdminUser = Depends(get_current_admin)):
    return current_admin
