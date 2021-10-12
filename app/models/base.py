import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.database import Base


class AbstractBase(Base):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_dt = sa.Column('create_dt', postgresql.TIMESTAMP(timezone=True), server_default=sa.func.now())
    update_dt = sa.Column('update_dt', postgresql.TIMESTAMP(timezone=True), onupdate=sa.func.now())
