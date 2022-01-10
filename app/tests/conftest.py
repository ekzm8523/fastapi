from typing import Generator, AsyncIterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.container import ApplicationContainer
import pytest

import os
os.environ["STAGE"] = "testing"


@pytest.fixture(scope="session")
async def container() -> AsyncIterable[ApplicationContainer]:
    print("==========Application set up start==========")
    from app.main import container  # lazy import
    await container.db.create_database()

    yield container

    print("==========Application tear down==========")
    await container.db.delete_database()
    container.db.low_level_delete_database()


@pytest.fixture(scope="function")
async def db(container: ApplicationContainer) -> AsyncIterable[Session]:
    connection = container.db.get_connection()
    transaction = connection.begin()

    session_factory = container.db.get_session_factory()
    session = session_factory()
    try:
        yield session
    finally:
        session.close()

    transaction.rollback()
    connection.close()



