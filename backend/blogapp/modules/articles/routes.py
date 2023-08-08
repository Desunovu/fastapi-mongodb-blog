from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from .models import ArticleCreate, ArticleResponse, ArticleDocument
from ..users.model import UserBase
from ...core.security.roles import RolesEnum
from ...core.security.utilities import RoleChecker, get_user_by_username

router = APIRouter(prefix="/articles")


@router.post("/", response_model=ArticleResponse)
async def create_article(
    create_article_body: ArticleCreate,
    current_user: Annotated[
        UserBase, Depends(RoleChecker(allowed_role=RolesEnum.AUTHOR.value))
    ],
):
    print(create_article_body.model_dump())
    author = await get_user_by_username(current_user.username)
    article = ArticleDocument(
        author=current_user,
        created_at=datetime.utcnow(),
    )
    # await ArticleDocument.insert_one(article)
    return {"article": article.model_dump(exclude={"author"})}
