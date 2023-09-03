from datetime import datetime

from pydantic import EmailStr, Field

from ...core.security.roles import RolesEnum
from ...utils.extended_document import ExtendedDocument


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
