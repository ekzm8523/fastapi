from starlette import status
from starlette.responses import JSONResponse


class APIExceptionErrorCodes:
    INCORRECT_LOGIN_CREDENTIAL = 'user_auth_invalid'
    INCORRECT_LOGIN_ID = 'incorrect_login_email'
    INVALID_TOKEN = 'user_token_invalid'
    EXPIRED_CREDENTIAL = 'user_auth_exp'
    UNAUTHORIZED_ACCESS = 'unauthorized'
    INCORRECT_TERM_AND_CONDITION = 'user_term_condition_invalid'
    MISMATCH_SELECTED_TYPE_AND_FILE = 'contents_upload_mismatch'
    USER_PROBLEM_TRIAL_EXCEEDED = 'trial_limit_exceeded'
    USER_PROBLEM_COMPLETED = 'problem_solved'
    PASSWORD_CONFIRMATION_ERROR = 'password_unmatch'
    USER_NOT_APPLICABLE_FOR_EXAM = 'not_applicable_for_exam'
    INVALID_EXCEL_CONTENT = 'invalid_excel_content'


class APIException(Exception):
    def __init__(
            self,
            status_code: int = 500,
            error_code: str = 'error',
            detail: any = '',
            _type: any = '',
            data=None
    ):
        self.status_code = int(status_code)
        self.error_code = error_code
        self.detail = detail
        self._type = _type
        self.data = data


def get_unauthorization_response(code=APIExceptionErrorCodes.UNAUTHORIZED_ACCESS, detail="unauthorized access"):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "vendor": "ai-tools",
            "type": "Authentication",
            "code": code,
            "message": detail,
            "detail": detail
        }
    )
