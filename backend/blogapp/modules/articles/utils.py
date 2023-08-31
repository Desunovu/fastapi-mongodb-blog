from fastapi import HTTPException
from starlette import status

from ..users.models import UserDocument
from ...core.security.roles import RolesEnum


def check_user_can_modify_document(
    document_author: UserDocument,
    user: UserDocument,
) -> UserDocument:
    """
    Проверяет, может ли пользователь редактировать документ.
    :return: UserDocument
    :raise HTTPException: если нет прав на изменение
    """
    # Разрешить администратору или владельцу
    if user.role == RolesEnum.ADMIN or document_author.id == user.id:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
