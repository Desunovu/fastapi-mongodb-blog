from fastapi import HTTPException
from starlette import status

from .models import ArticleDocument
from ..users.model import UserDocument
from ...core.security.roles import RolesEnum


def can_modify_article(article: ArticleDocument, user: UserDocument):
    """
    Проверяет может ли пользователь редактировать статью.
    :return: True
    :raise HTTPException 403: Если нет прав на изменение
    """
    if user.role == RolesEnum.ADMIN or article.author.id == user.id:
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
