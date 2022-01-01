
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from typing import Callable
from contextlib import contextmanager, AbstractContextManager
from app.models import Base
import logging


logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url)
        self._session_factory = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self._engine))

    async def create_database(self) -> None:
        """
        create_all을 실행시 engine에 연결된 DB에 Base를 상속받은 테이블들이 생성됩니다.
        """
        Base.metadata.create_all(bind=self._engine)

    async def delete_database(self) -> None:
        Base.metadata.drop_all(bind=self._engine)  # drop database

    @contextmanager
    async def get_session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception !!")
            session.rollback()
            raise
        finally:
            session.close()
