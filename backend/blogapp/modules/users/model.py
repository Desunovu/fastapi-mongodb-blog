from datetime import datetime

from beanie import Document

from pydantic import EmailStr



class UserDocument(Document):
    username: str
    password_hash: str
    email: EmailStr
    disabled: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Settings:
        name = "users"
