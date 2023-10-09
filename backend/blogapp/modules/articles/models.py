from datetime import datetime
from enum import Enum
from typing import Annotated

import pymongo
from beanie import Link
from pydantic import BaseModel, model_validator, Field

from ..users.models import UserDocument
from ...core.config import ARTICLE_MAX_LENGTH
from ...utils.extended_document import ExtendedDocument


class ArticleDocument(ExtendedDocument):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    author: Link[UserDocument] | None = None

    class Settings:
        name = "articles"
        indexes = [
            [
                ("title", pymongo.TEXT),
                ("content", pymongo.TEXT),
            ]
        ]


class ArticleCreateOrUpdate(BaseModel):
    title: Annotated[str, Field(min_length=2, max_length=120)] | None = None
    content: Annotated[str, Field(max_length=ARTICLE_MAX_LENGTH)] | None = None
    tags: Annotated[list[str], Field(max_items=20)] | None = None

    @model_validator(mode="after")
    def check_not_all_attributes_is_none(self):
        if not self.model_fields_set:
            raise ValueError("Model must have at least one not None field")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Article Title",
                    "content": "Article Text",
                    "tags": ["One", "Two"],
                }
            ]
        }
    }


class ArticleResponse(BaseModel):
    article: ArticleDocument


class ArticlesResponse(BaseModel):
    articles: list[ArticleDocument]


class ArticlesSortField(str, Enum):
    created_at = "created_at"
    title = "title"
