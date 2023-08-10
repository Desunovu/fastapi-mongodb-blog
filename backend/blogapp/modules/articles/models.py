from datetime import datetime

from beanie import Document, Link
from pydantic import BaseModel

from ..users.model import UserDocument


class ArticleDocument(Document):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    author: Link[UserDocument] | None = None

    class Settings:
        name = "articles"


class ArticleCreateOrUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Article Title",
                    "content": "Article Text",
                    "tags": [],
                }
            ]
        }
    }


class ArticleResponse(BaseModel):
    article: ArticleDocument
