import random

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import sessionmaker, Session
from typing import Callable
from contextlib import AbstractContextManager
from app.models import Base
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_url: str, testing: bool = False) -> None:
        self._engine = create_engine(db_url)
        self.db_name = db_url.rsplit('/', 1)[-1]
        if testing:
            self.db_name += f"_test{random.randint(0, 9999)}"
            self._low_level_create_database()
            test_db_url = db_url.rsplit('/', 1)[0] + '/' + self.db_name
            self._engine = create_engine(test_db_url)

        self._session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    async def create_database(self) -> None:
        """
        create_all을 실행시 engine에 연결된 DB에 Base를 상속받은 테이블들이 생성됩니다.
        """
        print("create db")
        Base.metadata.create_all(bind=self._engine)

    async def delete_database(self) -> None:
        Base.metadata.drop_all(bind=self._engine)  # drop database
        self._engine.dispose()

    # @contextmanager
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

    def get_connection(self) -> Connection:
        return self._engine.connect()

    def get_engine(self) -> Engine:
        return self._engine

    def set_engine(self, engine: Engine) -> None:
        self._engine = engine

    def _low_level_create_database(self):
        with self.get_connection() as conn:
            conn.execute("commit")
            self._engine.dispose()  # 이전에 쓰던 DB engine 반납
            conn.execute(f"create database {self.db_name}")

    def low_level_delete_database(self):  # 어쩔수 없이 끝나고 호출해야 하므로 protect underbar 제거
        with self.get_connection() as conn:
            conn.execute("commit")
            self._engine.dispose()  # testing DB engine 반납
            conn.execute(f"drop database {self.db_name}")
