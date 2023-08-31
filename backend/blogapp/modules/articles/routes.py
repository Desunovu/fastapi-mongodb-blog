from datetime import datetime
from typing import Annotated

from beanie import PydanticObjectId
from beanie.odm.enums import SortDirection
from fastapi import APIRouter, Depends, Query

from .models import (
    ArticleCreateOrUpdate,
    ArticleResponse,
    ArticleDocument,
    ArticlesResponse,
    ArticlesSortField,
)
from ..users.models import UserDocument
from ...core.database.extended_document import (
    delete_document_by_id,
    update_document_by_id,
)
from ...core.security.roles import RolesEnum
from ...core.security.utilities import RoleChecker

router = APIRouter(prefix="/articles")


@router.get("/", response_model=ArticlesResponse)
async def list_articles(
    _current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    skip: Annotated[int | None, Query(ge=0)] = None,  # >= 0
    limit: Annotated[int | None, Query(ge=1)] = None,  # >= 1
    sort_by: Annotated[ArticlesSortField, Query()] = ArticlesSortField.created_at.value,
    sort_order: Annotated[SortDirection, Query()] = SortDirection.DESCENDING.value,
):
    """Возвращает список статей."""

    # TODO добавить проекции
    # Получение списка статей
    articles = (
        await ArticleDocument.find(fetch_links=True)
        .sort((sort_by, sort_order))
        .skip(n=skip)
        .limit(n=limit)
        .to_list(length=None)
    )

    return {"articles": articles}


@router.post("/", response_model=ArticleResponse)
async def create_article(
    article_data: ArticleCreateOrUpdate,
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.AUTHOR.value))
    ],
):
    """Создает новую статью."""
    # Создание документа
    article = ArticleDocument(
        author=current_user,
        created_at=datetime.utcnow(),
        **article_data.model_dump(),
    )
    # Вставка документа
    await ArticleDocument.insert_one(article)

    return {"article": article}


@router.get("/{article_id}", response_model=ArticleResponse)
async def read_article(
    article_id: PydanticObjectId,
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
):
    """Возвращает статью по ее uuid."""

    # Получение данных
    article = await ArticleDocument.get_or_404(
        document_id=article_id, fetch_links=False
    )
    return {"article": article}


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: PydanticObjectId,
    article_data: ArticleCreateOrUpdate,
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.AUTHOR.value))
    ],
):
    """Обновляет статью по id"""

    article = update_document_by_id(
        document_id=article_id,
        current_user=current_user,
        update_data=article_data,
    )

    return {"article": article}


@router.delete("/{article_id}")
async def delete_article(
    article_id: PydanticObjectId,
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.AUTHOR.value))
    ],
):
    """Удаляет статью по ее uuid"""

    delete_response = delete_document_by_id(
        document_id=article_id, current_user=current_user
    )

    return delete_response
