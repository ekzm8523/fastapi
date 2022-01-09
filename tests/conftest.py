from typing import Generator

from sqlalchemy import create_engine

from app.container import ApplicationContainer
import pytest

import os
# @pytest.fixture(scope="session")
# def db_engine() -> Generator:
#     print("=============engine set up============")


@pytest.fixture(scope="session")
async def test_container() -> ApplicationContainer:
    print("==========Application set up start==========")
    os.environ["STAGE"] = "testing"
    from app.main import container  # lazy import
    await container.db.create_database()

    yield container

    print("==========Application tear downㅌ==========")
    await container.db.delete_database()
    container.db.low_level_delete_database()


# @pytest.fixture(scope="function")
# async def db()