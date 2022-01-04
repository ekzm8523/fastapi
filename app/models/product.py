import sqlalchemy as sa
from app.models import AbstractBase


class Product(AbstractBase):
    name: str = sa.Column(sa.String(length=30), nullable=False)

