from app.core.config import DatabaseSettings
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration


class ApplicationContainer(DeclarativeContainer):
    config = Configuration()
    config.from_pydantic(DatabaseSettings())


