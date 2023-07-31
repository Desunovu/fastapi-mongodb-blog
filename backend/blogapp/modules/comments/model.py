from datetime import datetime

from beanie import Document, Link

from ..authentication.model import User


class Comment(Document):
    content: str
    author: Link[User]
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "comments"
