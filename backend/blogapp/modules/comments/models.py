from datetime import datetime

from beanie import Link

from ..users.models import UserDocument
from ...core.database.extended_document import ExtendedDocument


class CommentDocument(ExtendedDocument):
    content: str
    author: Link[UserDocument]
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "comments"
