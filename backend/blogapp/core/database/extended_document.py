from beanie import Document, PydanticObjectId
from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from backend.blogapp.modules.articles.utils import check_user_can_modify_document
from backend.blogapp.modules.users.models import UserDocument


class ExtendedDocument(Document):
    """Подкласс Document из библиотеки beanie с дополнительными методами для расширенного функционала."""

    @classmethod
    async def get_or_404(cls, document_id, fetch_links=False):
        """
        Извлекает и возвращает документ через Document.get().
        Если документ не найден - поднимает исключение HTTPException с кодом состояния 404.
        """
        document = await cls.get(document_id=document_id, fetch_links=fetch_links)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
            )
        return document


def delete_document_by_id(
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
