
from app.schemas import UserAccountForm
from sqlalchemy.orm import Session
from app.models import User
import bcrypt
from app.exceptions import APIException, APIExceptionErrorCodes
from starlette import status
from jose import jwt
from datetime import datetime
from app.settings import JWT_AUTH
import uuid


def verify_password(request_password, hashed_password):
    return bcrypt.checkpw(request_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_hashed_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def authenticate(account_info: UserAccountForm, db: Session) -> User:

    user = db.query(User).filter_by(email=account_info.email).one()

    if not user:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=APIExceptionErrorCodes.INCORRECT_LOGIN_ID,
            detail="이메일을 확인해주세요!!"
        )

    if not verify_password(account_info.password, user.password):
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=APIExceptionErrorCodes.PASSWORD_CONFIRMATION_ERROR,
            detail="비밀번호를 확인해주세요!!"
        )

    return user


def create_access_token(user: User):
    jwt_info = {
        "typ": 'access_token',
        "email": user.email,
        "iss": JWT_AUTH['JWT_ISSUER'],  # issur 토큰 발급자
        "jti": uuid.uuid4().hex,  # JWT의 고유 식별자, 중복처리
        "exp": datetime.utcnow() + JWT_AUTH['JWT_EXPIRATION_DELTA'],  # 만료 기간
        "iat": datetime.utcnow(),  # 토큰이 발급된 시간 (issued at)
    }

    return jwt.encode(jwt_info, JWT_AUTH['JWT_SECRET_KEY'], algorithm=JWT_AUTH['JWT_ALGORITHM'])



def create_refresh_token(user: User):
    jwt_info = {
        "typ": 'refresh_token',
        "email": user.email,
        "iss": JWT_AUTH['JWT_ISSUER'],  # issur 토큰 발급자
        "jti": uuid.uuid4().hex,  # JWT의 고유 식별자, 중복처리
        "exp": datetime.utcnow() + JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA'],  # refresh 가능한 기간
        "iat": datetime.utcnow(),  # 토큰이 발급된 시간 (issued at)
    }

    return jwt.encode(jwt_info, JWT_AUTH['JWT_SECRET_KEY'], algorithm=JWT_AUTH['JWT_ALGORITHM'])
