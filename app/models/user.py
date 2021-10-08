import sqlalchemy as sa
import uuid
from sqlalchemy.dialects import postgresql

from app.models.base import AbstractBase

class User(AbstractBase):
    __tablename__ = "user"

    uuid = sa.Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4().hex, unique=True)
    email = sa.Column(sa.String(length=128), unique=True)
    password = sa.Column(sa.String(length=128))
