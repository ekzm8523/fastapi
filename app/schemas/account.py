from pydantic.main import BaseModel


class RegisterUserForm(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "your_email",
                "password": "your_password"
            }
        }


class LoginForm(BaseModel):
    email: str
    password: str