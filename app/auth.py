
from app.schemas import UserAccountForm
from sqlalchemy.orm import Session
from app.models import User
import bcrypt
from app.exceptions import APIException, APIExceptionErrorCodes
from starlette import status
from jose import jwt


def verify_password(request_password, hashed_password):
    return bcrypt.checkpw(request_password.encode('utf-8'), hashed_password)


async def authenticate(account_info: UserAccountForm, db: Session) -> User:

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

# def create_access_token()
