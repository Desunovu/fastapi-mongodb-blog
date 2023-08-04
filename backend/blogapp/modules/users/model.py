from datetime import datetime

from beanie import Document
from pydantic import EmailStr

from ...core.security.roles import RolesEnum


class UserDocument(Document):
    username: str
    password_hash: str
    email: EmailStr
    role: RolesEnum | None = None
    disabled: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Settings:
        name = "users"
