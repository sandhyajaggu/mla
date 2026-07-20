from app.crud.base import CRUDBase
from app.models.contact_message import ContactMessage
from app.schemas.contact_message import ContactMessageCreate, ContactMessageUpdate

contact = CRUDBase[ContactMessage, ContactMessageCreate, ContactMessageUpdate](ContactMessage)
