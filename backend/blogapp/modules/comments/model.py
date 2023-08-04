from datetime import datetime

from beanie import Document, Link

from ..users.model import UserDocument


class CommentDocument(Document):
    content: str
    author: Link[UserDocument]
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "comments"
