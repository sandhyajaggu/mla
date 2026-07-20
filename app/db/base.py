"""
Imports every model so Alembic's autogenerate can discover them via
Base.metadata. This file is imported by alembic/env.py — it is not used
directly anywhere else, but must import ALL models or migrations will
silently miss tables.
"""
from app.db.base_class import Base  # noqa
from app.models.admin_user import AdminUser  # noqa
from app.models.scheme import Scheme  # noqa
from app.models.cmrf_beneficiary import CmrfBeneficiary  # noqa
from app.models.development_work import DevelopmentWork, DevelopmentImage  # noqa
from app.models.media import MediaItem  # noqa
from app.models.gallery_item import GalleryItem  # noqa
from app.models.achievement import Achievement  # noqa
from app.models.contact_message import ContactMessage  # noqa
from app.models.voter_stat import VoterStat, ConstituencyInfo  # noqa
