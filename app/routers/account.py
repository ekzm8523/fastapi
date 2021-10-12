from fastapi import Depends
from fastapi.routing import APIRouter
from app.settings import DEVELOP_MODE
from app.schemas import UserAccountForm, LoginResponseForm
from sqlalchemy.orm import Session
import uuid, bcrypt
from app.database import get_db_sess
from app.models import User
from starlette.responses import Response
from starlette import status
account_router = APIRouter(
    prefix=f'/{DEVELOP_MODE}/api',
    tags=["account"]
)

@account_router.post("/register")
async def register(request_data: UserAccountForm, db: Session = Depends(get_db_sess)):

    try:
        hashed_password = bcrypt.hashpw(
            password=request_data.password.encode('utf-8'),
            salt=bcrypt.gensalt()
        )

        new_user = User(
            email=request_data.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        return Response(status_code=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        raise Exception

from app.auth import authenticate

@account_router.post("/login", response_model=LoginResponseForm)
async def login(request_data: UserAccountForm, db: Session = Depends(get_db_sess)):
    user = await authenticate(request_data, db)
    # access_token


    # access_token, refresh token = get_token
    # return token, email, 등등
    ...


    # 1. login 가능한지 확인
    # 2. access token, refresh token 생성
    # 함께 return