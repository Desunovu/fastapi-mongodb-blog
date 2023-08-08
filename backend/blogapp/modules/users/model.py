from datetime import datetime

from beanie import Document
from pydantic import EmailStr, BaseModel, Field

from ...core.security.roles import RolesEnum


class UserBase(BaseModel):
    """Базовая модель пользователя"""

    username: str
    email: EmailStr
    role: RolesEnum | None = None
    disabled: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserDocument(UserBase, Document):
    password_hash: str = Field(exclude=True)

    class Settings:
        name = "users"
