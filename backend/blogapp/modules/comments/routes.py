from datetime import datetime
from typing import Annotated

from beanie import PydanticObjectId, Link
from beanie.odm.enums import SortDirection
from bson import DBRef
from fastapi import APIRouter, Depends, Query

from .models import (
    CommentsSortField,
    CommentsResponse,
    CommentDocument,
    CommentCreate,
    CommentResponse,
    ReplyCreate,
    CommentUpdate,
)
from ..articles.models import ArticleDocument
from ..users.models import UserDocument
from ...core.security.roles import RolesEnum
from ...core.security.utilities import RoleChecker

router = APIRouter(prefix="/comments")


@router.get("/", response_model=CommentsResponse)
async def list_comments(
    _current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    article_id: PydanticObjectId,
    skip: Annotated[int | None, Query(ge=0)] = None,  # >= 0
    limit: Annotated[int | None, Query(ge=1)] = None,  # >= 1
    sort_by: Annotated[CommentsSortField, Query()] = CommentsSortField.created_at.value,
    sort_order: Annotated[SortDirection, Query()] = SortDirection.DESCENDING.value,
):
    """Возвращает список комментариев к статье"""
    # Поиск статьи
    _article = await ArticleDocument.get_or_404(document_id=article_id)
    # Поиск комментариев
    comments = (
        await CommentDocument.find(
            CommentDocument.article.id == article_id,
            # TODO FIX BUG с fetch в версии beanie 1.21
            fetch_links=True,
        )
        .sort((sort_by, sort_order))
        .skip(n=skip)
        .limit(n=limit)
        .to_list(length=None)
    )

    return {"comments": comments}


@router.post("/", response_model=CommentResponse)
async def create_comment(
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    comment_data: CommentCreate,
):
    """Создает новый комментарий к статье."""
    # Поиск статьи
    article = await ArticleDocument.get_or_404(document_id=comment_data.article_id)
    # Создание документа комментария
    comment = CommentDocument(
        author=current_user,
        article=article,
        replies=[],
        created_at=datetime.utcnow(),
        **comment_data.model_dump(),
    )
    # Вставка документа комментария
    await comment.insert()

    return {"comment": comment}


@router.post("/reply", response_model=CommentResponse)
async def create_reply(
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    reply_data: ReplyCreate,
):
    """Создает комментарий-ответ на комментарий"""
    # Поиск комментария для ответа
    parent_comment = await CommentDocument.get_or_404(
        document_id=reply_data.parent_comment_id
    )
    # Создание документа ответа
    reply = CommentDocument(
        author=current_user,
        is_reply=True,
        created_at=datetime.utcnow(),
        **reply_data.model_dump(),
    )
    # Вставка документа ответа и обновление списка ответов
    await reply.insert()
    parent_comment.replies.append(
        Link(
            DBRef(id=reply.id, collection=reply.get_collection_name()),
            document_class=CommentDocument,
        )
    )
    await parent_comment.save()

    return {"comment": reply}
