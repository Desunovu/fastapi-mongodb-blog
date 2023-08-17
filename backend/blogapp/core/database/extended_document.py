from beanie import Document
from fastapi import HTTPException
from starlette import status


class ExtendedDocument(Document):
    """Подкласс Document из библиотеки beanie с дополнительными методами для расширенного функционала."""

    @classmethod
    async def get_or_404(cls, document_id, fetch_links=True):
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
