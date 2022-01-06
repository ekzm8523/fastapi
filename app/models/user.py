import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.mutable import MutableDict
from app.models import AbstractBase


class User(AbstractBase):
    __abstract__ = True

    name: str = sa.Column(sa.String(length=30), nullable=False)
    email: str = sa.Column(sa.String(length=50), nullable=False)
    password: str = sa.Column(sa.String(length=30), nullable=False)
    phone_number: str = sa.Column(sa.String(length=15), nullable=False)
    gender: int = sa.Column(sa.SmallInteger, nullable=False)


class Admin(User):
    level: int = sa.Column(sa.SmallInteger, nullable=False)  # 권한


class Customer(User):
    birthday: str = sa.Column(sa.String(length=30), nullable=False)
    address: dict[str, str] = sa.Column(MutableDict.as_mutable(postgresql.JSONB), nullable=False)
    point: int = sa.Column(sa.Integer, default=0)
