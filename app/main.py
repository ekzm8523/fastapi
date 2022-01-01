from typing import Optional
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from app.core.config import ApplicationSettings
from app.database import Database


app: FastAPI = FastAPI()


@app.on_event('startup')
async def startup_event():
    print("start up fastapi")
    app.settings = ApplicationSettings()
    app.db = Database(db_url=app.settings.db.get_url())
    await app.db.create_database()


@app.on_event('shutdown')
async def shutdown_event():
    print("delete database complete")
    await app.db.delete_database()


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)







