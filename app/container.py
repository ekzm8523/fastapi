from app.core.config import DatabaseSettings
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
# from dependency_injector.providers import Configuration
from dependency_injector import providers

from app.database import Database


class ApplicationContainer(DeclarativeContainer):
    config = providers.Configuration()
    config.from_pydantic(DatabaseSettings())
    db = providers.Singleton(Database, db_url=config.get_url())


