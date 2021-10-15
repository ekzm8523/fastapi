from fastapi import Depends
from fastapi.routing import APIRouter
from app.settings import DEVELOP_MODE
from app.schemas import UserAccountForm, LoginResponseForm
from sqlalchemy.orm import Session
import uuid, bcrypt
from app.database import get_db_sess
from app.models import User, RefreshToken
from starlette.responses import Response, JSONResponse
from starlette import status
from app.auth import authenticate, create_access_token, create_refresh_token


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
            password=hashed_password.decode('utf-8')
        )

        db.add(new_user)
        db.commit()
        return Response(status_code=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        raise Exception


@account_router.post("/login", response_model=LoginResponseForm)
async def login(request_data: UserAccountForm, db: Session = Depends(get_db_sess)):

    user = authenticate(request_data, db)

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    header, payload, signature = refresh_token.split('.')

    refresh_token_instance = RefreshToken(
        header=header,
        payload=payload,
        signature=signature
    )

    if user.refresh_token:
        db.delete(user.refresh_token)
        db.commit()
    user.refresh_token = refresh_token_instance
    db.add(refresh_token_instance)
    db.commit()

    return JSONResponse({
        'access_token': access_token,
        'refresh_token': refresh_token,
        },
        status_code=status.HTTP_200_OK
    )
