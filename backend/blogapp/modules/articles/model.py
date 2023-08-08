from datetime import datetime

from beanie import Document, Link

from ..users.model import UserDocument


class ArticleDocument(Document):
    title: str
    content: str
    author: Link[UserDocument]
    tags: list[str]
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "articles"
