from datetime import datetime

from beanie import Document, Link
from pydantic import BaseModel

from ..users.model import UserDocument


class ArticleBase(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None


class ArticleDocument(ArticleBase, Document):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    author: Link[UserDocument] | None = None

    class Settings:
        name = "articles"


class ArticleCreate(ArticleBase):
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


class ArticleUpdate(ArticleBase):
    pass


class ArticleResponse(BaseModel):
    article: ArticleDocument
