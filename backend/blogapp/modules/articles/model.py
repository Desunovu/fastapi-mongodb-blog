from datetime import datetime
from typing import List, Optional

from beanie import Document, Link

from ..tags.model import TagDocument
from ..users.model import UserDocument


class ArticleDocument(Document):
    title: str
    content: str
    author: Link[UserDocument]
    tags: Optional[List[Link[TagDocument]]]
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "articles"
