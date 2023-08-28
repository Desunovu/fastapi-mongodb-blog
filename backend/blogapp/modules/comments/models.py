from datetime import datetime
from enum import Enum

from beanie import Link, PydanticObjectId
from pydantic import BaseModel, Field

from ..articles.models import ArticleDocument
from ..users.models import UserDocument
from ...core.database.extended_document import ExtendedDocument


class CommentDocument(ExtendedDocument):
    content: str
    author: Link[UserDocument]
    disabled: bool = False
    is_reply: bool = False
    article: Link[ArticleDocument] | None = Field(None, exclude=True)
    # TODO Вернуть Optional None к replies после выхода исправления бага fetch в beanie
    replies: list[Link["CommentDocument"]] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Settings:
        name = "comments"


class CommentCreateOrUpdate(BaseModel):
    article_id: PydanticObjectId = Field(..., exclude=True)
    content: str = Field(..., min_length=2, max_length=120)


class ReplyCreateOrUpdate(BaseModel):
    parent_comment_id: PydanticObjectId = Field(..., exclude=True)
    content: str = Field(..., min_length=2, max_length=120)


class CommentsResponse(BaseModel):
    comments: list[CommentDocument]


class CommentResponse(BaseModel):
    comment: CommentDocument


class CommentsSortField(str, Enum):
    created_at = "created_at"
