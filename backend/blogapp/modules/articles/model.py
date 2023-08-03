from datetime import datetime
from typing import List, Optional

from beanie import Document, Link

from ..users.model import User
from ..tags.model import Tag


class Article(Document):
    title: str
    content: str
    author: Link[User]
    tags: Optional[List[Link[Tag]]]
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "articles"
