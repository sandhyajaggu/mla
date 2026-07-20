from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.crud.crud_contact import contact as crud_contact
from app.models.admin_user import AdminUser
from app.schemas.contact_message import ContactMessageCreate, ContactMessageOut, ContactMessageUpdate

router = APIRouter()


@router.post("", response_model=ContactMessageOut, status_code=status.HTTP_201_CREATED)
def submit_contact_message(payload: ContactMessageCreate, db: Session = Depends(get_db)):
    """Public — Contact.js submit. Anyone can send a message, no auth needed."""
    return crud_contact.create(db, obj_in=payload.model_dump())


@router.get("", response_model=list[ContactMessageOut])
def list_contact_messages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    """Admin only — AdminContactus.js inbox."""
    return crud_contact.get_multi(db, skip=skip, limit=limit)


@router.patch("/{message_id}", response_model=ContactMessageOut)
def mark_contact_message(
    message_id: int,
    payload: ContactMessageUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    """Admin only — mark a message as read/unread."""
    obj = crud_contact.get(db, message_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Message not found")
    return crud_contact.update(db, db_obj=obj, obj_in=payload.model_dump())


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact_message(
    message_id: int, db: Session = Depends(get_db), _: AdminUser = Depends(get_current_admin)
):
    obj = crud_contact.remove(db, id=message_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Message not found")
