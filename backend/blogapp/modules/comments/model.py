from datetime import datetime

from beanie import Document, Link

from ..users.model import User


class Comment(Document):
    content: str
    author: Link[User]
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "comments"
