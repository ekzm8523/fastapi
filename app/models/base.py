import uuid
from uuid import UUID

from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any, Union
import sqlalchemy as sa
import re

from sqlalchemy.orm import declarative_mixin


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return f"mms_{'_'.join(list(map(str.lower, re.findall('([A-Z][a-z]+)', cls.__name__))))}"


@declarative_mixin
class TimestampMixin:
    create_dt = sa.Column("create_dt", postgresql.TIMESTAMP, server_default=sa.func.now())
    update_dt = sa.Column(
        "update_dt",
        postgresql.TIMESTAMP,
        server_default=sa.func.now(),
        onupdate=sa.func.current_timestamp()
    )


class AbstractBase(Base, TimestampMixin):
    __abstract__ = True

    id: Union[UUID, sa.Column] = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)



