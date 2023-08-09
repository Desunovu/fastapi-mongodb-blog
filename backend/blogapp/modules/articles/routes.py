from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from .models import ArticleCreateOrUpdate, ArticleResponse, ArticleDocument, ArticleBase
from ..users.model import UserDocument
from ...core.security.roles import RolesEnum
from ...core.security.utilities import RoleChecker

router = APIRouter(prefix="/articles")


@router.post("/", response_model=ArticleResponse)
async def create_article(
    article_data: ArticleCreateOrUpdate,
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.AUTHOR.value))
    ],
):
    article = ArticleDocument(
        author=current_user,
        created_at=datetime.utcnow(),
        **article_data.model_dump(),
    )
    await ArticleDocument.insert_one(article)
    return {"article": ArticleBase(**article.dict())}
