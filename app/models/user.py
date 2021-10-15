import sqlalchemy as sa
import uuid
from sqlalchemy.dialects import postgresql

from app.models.base import AbstractBase
from sqlalchemy.orm import relationship

class User(AbstractBase):
    __tablename__ = "user"

    uuid = sa.Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4().hex, unique=True)
    email = sa.Column(sa.String(length=128), unique=True)
    password = sa.Column(sa.String(length=128))
    refresh_token = relationship("RefreshToken", back_populates="user", uselist=False)


class RefreshToken(AbstractBase):
    __tablename__ = "refresh_token"

    user = relationship("User", back_populates="refresh_token", uselist=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id", ondelete="SET NULL"))
    header = sa.Column(sa.String(length=128), unique=True)
    payload = sa.Column(sa.String(length=512), unique=True)
    signature = sa.Column(sa.String(length=128), unique=True)
