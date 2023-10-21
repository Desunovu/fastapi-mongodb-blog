from datetime import datetime
from enum import Enum
from typing import Annotated

import pymongo
from beanie import Link
from pydantic import BaseModel, model_validator, Field, field_validator

from ..users.models import UserDocument
from ...core.config import ARTICLE_MAX_LENGTH
from ...utils.extended_document import ExtendedDocument


class ArticleDocument(ExtendedDocument):
    title: str | None = None
    preview_image_url: str | None = None
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
    """Модель для создания или обновления статьи. Должно быть хотя бы одно поле не None"""

    title: Annotated[str, Field(min_length=2, max_length=120)] | None = None
    preview_image_url: Annotated[str, Field(max_length=120)] | None = None
    content: Annotated[str, Field(max_length=ARTICLE_MAX_LENGTH)] | None = None
    tags: Annotated[list[str], Field(max_items=20)] | None = None

    @model_validator(mode="after")
    def check_not_all_attributes_is_none(self):
        if not self.model_fields_set:
            raise ValueError("Model must have at least one not None field")
        return self

    @field_validator("preview_image_url")
    @classmethod
    def validate_preview_image_url(cls, preview_image_url: str) -> str:
        """Проверяет что стока - это URL-адрес изображения"""
        is_valid_protocol = preview_image_url.startswith(("http://", "https://"))
        is_valid_extension = preview_image_url.endswith((".jpg", ".png"))

        if not (is_valid_protocol and is_valid_extension):
            raise ValueError(
                "Preview image URL must be a valid file URL with .jpg or .png extension"
            )
        return preview_image_url

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Article Title",
                    "preview_image_url": "https://example.com/image.jpg",
                    "content": "Article Text",
                    "tags": ["One", "Two"],
                }
            ]
        }
    }


class ArticleResponse(BaseModel):
    """Модель ответа с одной статьей"""

    article: ArticleDocument


class ArticlesResponse(BaseModel):
    """Модель ответа с списком статей"""

    articles: list[ArticleDocument]
    total: int


class ArticlesSortField(str, Enum):
    """Поля по которым проводится сортировка"""

    created_at = "created_at"
    title = "title"
