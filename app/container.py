from fastapi import FastAPI

from app.core.config import ApplicationSettings
from app.database import Database


class ApplicationContainer:
    app: FastAPI
    db: Database
    settings: ApplicationSettings

    def __init__(self):
        self.app = FastAPI()
        self.settings = ApplicationSettings()
        testing = self.settings.stage == "testing"
        self.db = Database(db_url=self.settings.db.get_url(), testing=testing)
        if testing:
            self.settings.db.db = self.db.db_name
