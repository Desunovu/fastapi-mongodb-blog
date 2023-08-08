from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from .models import ArticleCreate, ArticleResponse, ArticleDocument
from ..users.model import UserDocument
from ...core.security.roles import RolesEnum
from ...core.security.utilities import RoleChecker

router = APIRouter(prefix="/articles")


@router.post("/", response_model=ArticleResponse)
async def create_article(
    create_article_data: ArticleCreate,
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.AUTHOR.value))
    ],
):
    article = ArticleDocument(
        author=current_user,
        created_at=datetime.utcnow(),
        **create_article_data.model_dump(),
    )
    await ArticleDocument.insert_one(article)
    return {"article": article}
