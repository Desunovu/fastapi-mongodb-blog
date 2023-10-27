from datetime import datetime

from beanie import Document, PydanticObjectId
from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

from ..core.security.models import UserBase
from ..core.security.roles import RolesEnum


class ExtendedDocument(Document):
    """Подкласс Document из библиотеки beanie с дополнительными методами для расширенного функционала."""

    def check_user_can_modify_document(self, current_user: UserBase) -> None:
        """
        Проверяет, может ли пользователь редактировать документ.
        :raise HTTPException: если нет прав на изменение
        """
        # Разрешить администратору
        if current_user.role == RolesEnum.ADMIN:
            return
        # Разрешить редактировать свой документ
        if current_user.id == self.id:
            return
        # Разрешить редактировать документы за своим авторством
        if hasattr(self, "author"):
            if current_user.id == self.author.id:
                return
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
        current_user: UserBase,
        update_data: BaseModel,
    ):
        """Обновляет документ по его ID. Перед выполнением вызывает check_user_can_modify_document"""

        # Получение данных
        document = await cls.get_or_404(document_id=document_id, fetch_links=True)
        # Проверка прав редактирования
        document.check_user_can_modify_document(current_user)
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
        current_user: UserBase,
        link_fields_to_delete: list[str] | None = None,
    ) -> Response:
        """Удаляет документ по его ID. Перед выполнением вызывает check_user_can_modify_document"""

        # Поиск документа
        document = await cls.get_or_404(document_id=document_id, fetch_links=True)
        # Проверка прав редактирования
        document.check_user_can_modify_document(current_user)
        # Удаление ссылок
        if link_fields_to_delete:
            for field_name in link_fields_to_delete:
                document_field_to_delete = getattr(document, field_name, None)
                if isinstance(document_field_to_delete, list):
                    for link in document_field_to_delete:
                        await link.delete()
                elif isinstance(document_field_to_delete, ExtendedDocument):
                    await document_field_to_delete.delete()
        # Удаление документа
        delete_result = await document.delete()

        if delete_result:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        # Исключение на случай если не получен delete_result
        raise HTTPException(status_code=status.HTTP_410_GONE)
