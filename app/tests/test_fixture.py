import pytest
from sqlalchemy.orm import Session

from app.container import ApplicationContainer


@pytest.mark.asyncio
async def test_container_fixture(container: ApplicationContainer):
    print()


@pytest.mark.asyncio
async def test__db_fixture(db: Session):
    print()