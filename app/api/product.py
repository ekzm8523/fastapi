
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.main import container
product_router = APIRouter()


@product_router.post("/product")
async def create_product(db: Session = Depends(container.db.get_session)):
    print("post 잘왔다")
