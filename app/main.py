from typing import Optional
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from app.container import ApplicationContainer
from app.database import Database
import sys

def create_app() -> FastAPI:
    container = ApplicationContainer()
    container.wire([sys.modules[__name__]])
    db = Database(db_url="")
    db.create_database()

    app = FastAPI()
    app.container = container
    app.include_router(...)
    return app


app: FastAPI = create_app()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
#
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_price": item.price, "item_id": item_id}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)







