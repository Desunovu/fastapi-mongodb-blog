from pydantic import BaseModel, Field

from ..articles.models import ArticleDocument


class ArticleGenerate(BaseModel):
    """Тело запроса для генерации статьи"""

    title: str = Field(
        ..., min_length=2, max_length=120, examples=["Разработка ПО для платы ESP32"]
    )
    tags: list[str] | None = Field(
        None, max_items=20, examples=[["Программирование", "ESP32"]]
    )
    key_phrases: list[str] | None = Field(
        None, max_items=20, examples=[["Среда разработки", "Обмен данными"]]
    )


class GeneratedArticleResponse(BaseModel):
    """Тело ответа для генерации статьи"""

    article: ArticleDocument
    tokens_used: int
