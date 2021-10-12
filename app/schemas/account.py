from pydantic.main import BaseModel


class UserAccountForm(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "your_email",
                "password": "your_password"
            }
        }


class LoginResponseForm(BaseModel):
    email: str
    access_token: str
    refresh_token: str

