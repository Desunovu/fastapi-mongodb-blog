from pydantic import BaseModel, EmailStr


class TokenResponseBody(BaseModel):
    """Ответ на запрос токена"""
    access_token: str
    token_type: str


class RegisterRequestBody(BaseModel):
    """Запрос регистрации"""
    username: str
    password: str
    email: EmailStr
