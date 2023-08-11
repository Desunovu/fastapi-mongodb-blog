from datetime import datetime
from typing import Annotated

from beanie import Link
from pydantic import BaseModel, model_validator, Field

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
    title: Annotated[str, Field(min_length=2, max_length=120)] | None = None
    content: Annotated[str, Field(max_length=120)] | None = None
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
