from datetime import datetime

from beanie import Document, Link
from pydantic import BaseModel, model_validator

from ..users.model import UserDocument
from ...core.database.extended_document import ExtendedDocument


class ArticleDocument(ExtendedDocument):
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

    @model_validator(mode="after")
    def check_not_all_attributes_is_none(self):
        if not self.model_fields_set:
            raise ValueError("Model must have at least one not None field")

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
