from datetime import datetime

from beanie import Document, PydanticObjectId, DeleteRules
from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

from ..core.security.roles import RolesEnum


class ExtendedDocument(Document):
    """Подкласс Document из библиотеки beanie с дополнительными методами для расширенного функционала."""

    def check_user_can_modify_document(
        self,
        current_user: "UserDocument",
    ) -> "UserDocument":
        """
        Проверяет, может ли пользователь редактировать документ.
        :return: UserDocument
        :raise HTTPException: если нет прав на изменение
        """
        # Разрешить администратору или владельцу
        if current_user.role == RolesEnum.ADMIN or self.author.id == current_user.id:
            return current_user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

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

    @classmethod
    async def update_document_by_id(
        cls,
        document_id: PydanticObjectId,
        current_user: "UserDocument",
        update_data: BaseModel,
    ):
        """Обновляет документ по его ID. У документа должен быть author."""

        # Получение данных
        document = await cls.get_or_404(document_id=document_id, fetch_links=True)
        # Проверка прав редактирования
        try:
            _current_user = document.check_user_can_modify_document(
                current_user=current_user
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Обновление данных
        document = document.model_copy(
            update=update_data.model_dump(exclude_unset=True)
        )
        document.updated_at = datetime.utcnow()
        await document.save()

        return document

    @classmethod
    async def delete_document_by_id(
        cls,
        document_id: PydanticObjectId,
        current_user: "UserDocument",
    ) -> Response:
        """Удаляет документ по его ID. У документа должен быть author."""

        # Поиск документа
        document = await cls.get_or_404(document_id=document_id, fetch_links=True)
        # Проверка прав редактирования
        try:
            _current_user = document.check_user_can_modify_document(
                current_user=current_user
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Удаление документа и всех ссылок
        delete_result = await document.delete(link_rule=DeleteRules.DELETE_LINKS)

        if delete_result:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        # Исключение на случай если не получен delete_result
        raise HTTPException(status_code=status.HTTP_410_GONE)
