from datetime import datetime

from beanie import Document
from pydantic import EmailStr, BaseModel

from ...core.security.roles import RolesEnum


class UserBaseModel(BaseModel):
    """Базовая модель пользователя"""

    username: str
    email: EmailStr
    role: RolesEnum | None = None
    disabled: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserDocument(UserBaseModel, Document):
    password_hash: str

    class Settings:
        name = "users"
