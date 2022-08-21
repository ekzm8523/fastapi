from datetime import datetime, timedelta
import httplib2
import jwt
from fastapi import APIRouter, Depends, HTTPException, requests
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.utils import get_openapi
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from google.oauth2 import id_token
from jwt import PyJWTError
from starlette.requests import Request
from oauth2client import client
from starlette.responses import JSONResponse, RedirectResponse
from starlette.status import HTTP_403_FORBIDDEN

from app.schemas import Token, User, OAuth2PasswordBearerCookie, TokenData
from app.main import container
from app.static import CLIENT_ID, ERROR_ROUTE

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")
#
# @router.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     data = form_data.parse()
#     print(data.user_name)
#     print(data.password)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "myemail@gmail.com",
        "disabled": False,
    }
}


def get_user_by_email(db, email: str):
    for username, value in db.items():
        if value.get("email") == email:
            user_dict = db[username]
            return User(**user_dict)


def authenticate_user_email(fake_db, email: str):
    user = get_user_by_email(fake_db, email)
    if not user:
        return False
    return user



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_email(fake_users_db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post(f"/oauth/callback", response_model=Token, tags=["security"])
async def swap_token(request: Request = None):
    if not request.headers.get("X-Requested-With"):
        raise HTTPException(status_code=400, detail="Incorrect headers")

    google_client_type = request.headers.get("X-Google-OAuth2-Type")

    if google_client_type == 'server':
        try:
            body_bytes = await request.body()
            auth_code = jsonable_encoder(body_bytes)
            credentials = client.credentials_from_code(
                client_id=container.settings.google.client_id,
                client_secret=container.settings.google.client_secret,
                scope=["profile", "email"],
                code=auth_code,
            )

            http_auth = credentials.authorize(httplib2.Http())
            email = credentials.id_token["email"]
        except:
            raise HTTPException(status_code=400, detail="Unable to validate social login")

    if google_client_type == 'client':
        body_bytes = await request.body()
        auth_code = jsonable_encoder(body_bytes)

        try:
            id_info = id_token.verify_oauth2_token(auth_code, requests.Request(), CLIENT_ID)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            if id_info['email'] and id_info['email_verified']:
                email = id_info.get('email')

            else:
                raise HTTPException(status_code=400, detail="Unable to validate social login")

        except:
            raise HTTPException(status_code=400, detail="Unable to validate social login")

    authenticated_user = authenticate_user_email(fake_users_db, email)

    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Incorrect email address")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": authenticated_user.email}, expires_delta=access_token_expires
    )

    token = jsonable_encoder(access_token)

    response = JSONResponse({"access_token": token, "token_type": "bearer"})

    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        domain="http://localhost:8000",
        max_age=1800,
        expires=1800,
    )

    return response

@router.get("/")
async def homepage():
    return "Welcome to the security test!"


@router.get(f"{ERROR_ROUTE}", tags=["security"])
async def login_error():
    return "Something went wrong logging in!"


@router.get("/logout", tags=["security"])
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization", domain="http://localhost:8000")
    return response


@router.get("/secure_endpoint", tags=["security"])
async def get_open_api_endpoint(current_user: User = Depends(get_current_active_user)):
    response = "How cool is this?"
    return response


@router.get("/users/me/", response_model=User, tags=["users"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/", tags=["users"])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]