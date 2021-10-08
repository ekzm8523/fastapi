from fastapi import Depends
from fastapi.routing import APIRouter
from app.settings import DEVELOP_MODE
from app.schemas import RegisterUserForm
from sqlalchemy.orm import Session

from app.database import get_db_sess

account_router = APIRouter(
    prefix=f'{DEVELOP_MODE}/api',
    tags=["account"]
)

@account_router.post("/register")
async def register(request_data: RegisterUserForm, db: Session = Depends(get_db_sess)):
    # 여기서 바로 user 생성
    pass

# @account_router.post("/login", response_model=LoginR)
# async def login("/login")
