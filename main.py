from typing import Optional
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from app import routers

from app.database import open_database_connection_pool, close_database_connection_pool

app = FastAPI()


@app.on_event('startup')
def startup_event():
    open_database_connection_pool()


@app.on_event('shutdown')
def shutdown_event():
    close_database_connection_pool()


app.include_router(router=routers.account_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)







