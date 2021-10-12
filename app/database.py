from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncIterable, Optional
from sqlalchemy.engine import Engine as Database
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import Depends

from app.settings import DATABASE_URL

Base = declarative_base()
_db_conn: Optional[Database]

# connection pool 이란 웹 컨테이너가 실행되면서 DB와 미리 connection 을 해놓은 객체들을 pool 에 저장해두었다가
# 클라이언트 요청이 오면 connection 을 빌려주고 처리가 끝나면 다시 connection 을 반납받아 pool 에 저장하는 방식을 말한다.
def open_database_connection_pool():
    global _db_conn
    _db_conn = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=_db_conn)
    return


def close_database_connection_pool():
    global _db_conn
    if _db_conn:
        _db_conn.dispose()


def get_db_conn() -> Database:
    assert _db_conn is not None, 'please check db connection'
    return _db_conn


def get_db_sess(db_conn=Depends(get_db_conn)) -> AsyncIterable[Session]:
    sess = Session(bind=db_conn)
    try:
        yield sess
    finally:
        sess.close()
