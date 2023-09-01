from datetime import datetime

from beanie import PydanticObjectId
from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

from ..core.database.extended_document import ExtendedDocument
from ..core.security.roles import RolesEnum
from ..modules.users.models import UserDocument


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


async def update_document_by_id(
    document_id: PydanticObjectId,
    current_user: UserDocument,
    update_data: BaseModel,
) -> ExtendedDocument:
    """Обновляет документ по его ID. У документа должен быть author."""

    # Получение данных
    document = await ExtendedDocument.get_or_404(document_id=document_id)
    # Проверка прав редактирования
    try:
        _current_user = check_user_can_modify_document(
            document_author=document.author, user=current_user
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Обновление данных
    document = document.model_copy(update=update_data.model_dump(exclude_unset=True))
    document.updated_at = datetime.utcnow()
    await document.save()

    return document


async def delete_document_by_id(
    document_id: PydanticObjectId, current_user: UserDocument
) -> Response:
    """Удаляет документ по его ID. У документа должен быть author."""

    # Поиск документа
    document = await ExtendedDocument.get_or_404(
        document_id=document_id, fetch_links=True
    )
    # Проверка прав редактирования
    try:
        _current_user = check_user_can_modify_document(
            document_author=document.author, user=current_user
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Удаление документа
    delete_result = await document.delete()

    if delete_result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Исключение на случай если не получен delete_result
    raise HTTPException(status_code=status.HTTP_410_GONE)
