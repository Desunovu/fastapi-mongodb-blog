from datetime import datetime

from pydantic import EmailStr, Field

from ...core.database.extended_document import ExtendedDocument
from ...core.security.roles import RolesEnum


class UserDocument(ExtendedDocument):
    username: str
    email: EmailStr
    role: RolesEnum | None = None
    disabled: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    password_hash: str | None = Field(default=None, exclude=True)

    class Settings:
        name = "users"
