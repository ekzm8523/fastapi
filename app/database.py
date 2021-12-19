
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any, Callable
from contextlib import contextmanager, AbstractContextManager
import re
import logging

logger = logging.getLogger(__name__)

@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{'_'.join(list(map(str.lower, re.findall('([A-Z][a-z]+)', cls.__name__))))}"


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url)
        self._session_factory = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self._engine))

    def create_database(self) -> None:
        """
        create_all을 실행시 engine에 연결된 DB에 Base를 상속받은 테이블들이 생성됩니다.
        """
        Base.metadata.create_all(bind=self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception !!")
            session.rollback()
            raise
        finally:
            session.close()
