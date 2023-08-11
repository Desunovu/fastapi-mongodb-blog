from fastapi import HTTPException
from starlette import status

from .models import ArticleDocument
from ..users.model import UserDocument
from ...core.security.roles import RolesEnum


def check_user_can_modify_article(
    article: ArticleDocument, user: UserDocument
) -> UserDocument:
    """
    Проверяет может ли пользователь редактировать статью.
    :return: UserDocument
    :raise HTTPException: если нет прав на изменение
    """
    # Разрешить администратору или владельцу
    if user.role == RolesEnum.ADMIN or article.author.id == user.id:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
