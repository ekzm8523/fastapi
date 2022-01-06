import uuid
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from app.models import AbstractBase
from app.utils.generation import generation_sn
from uuid import UUID


class Category(AbstractBase):
    name: str = sa.Column(sa.String(length=30), nullable=False)
    description: str = sa.Column(sa.String(length=100), nullable=False, default="", server_default="")


class Product(AbstractBase):
    category_id: UUID = sa.Column(sa.ForeignKey(f"{Category.__tablename__}.id"), nullable=False, index=True)
    category: Mapped[Category] = relationship(Category, backref="product_list")
    name: str = sa.Column(sa.String(length=30), nullable=False, index=True)
    sn: str = sa.Column(sa.String(length=10), nullable=False, default=generation_sn)
    manufacturer: str = sa.Column(sa.String(length=30), nullable=False)
    sold_count: int = sa.Column(sa.Integer, nullable=False)
    image: Optional[str] = sa.Column(sa.String(length=100))
    standard: str = sa.Column(sa.String(length=10), nullable=False)


class Sku(AbstractBase):
    product_id: UUID = sa.Column(sa.ForeignKey(f"{Product.__tablename__}.id"), nullable=False, index=True)
    product: Mapped[Product] = relationship(Product, backref="sku_list")
    name: str = sa.Column(sa.String(length=30), nullable=False)
    sku: str = sa.Column(sa.String(length=10), nullable=False, default=generation_sn)
    sold_count: int = sa.Column(sa.Integer, nullable=False, default=0)
    supply_count: int = sa.Column(sa.Integer, nullable=False)
    sell_price: int = sa.Column(sa.Integer, nullable=False)
    left_inventory: int = sa.Column(sa.Integer, nullable=False, default=0)
    setting_inventory: int = sa.Column(sa.Integer, nullable=False, default=0)

