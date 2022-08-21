
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.main import container
from app.models import Product
router = APIRouter()


@router.post("/product")
async def create_product(db: Session = Depends(container.db.get_session)):
    print("post 잘왔다")
    p = Product(name="test")
    db.add(p)
    db.commit()


