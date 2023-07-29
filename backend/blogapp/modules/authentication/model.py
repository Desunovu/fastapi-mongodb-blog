from datetime import datetime

from beanie import Document


class User(Document):
    username: str
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "users"
