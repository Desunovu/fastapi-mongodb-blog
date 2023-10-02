from core.config import AVATAR_PROVIDER_URL


def is_valid_avatar_url(avatar_url: str):
    """
    Проверяет, начинается ли указанный URL аватара с URL-адреса провайдера аватаров.

    Аргументы:
        avatar_url (str): URL аватара, который нужно проверить.

    Возвращает:
        bool: True, если URL аватара начинается с URL-адреса провайдера аватаров, в противном случае False.
    """
    if avatar_url.startswith(AVATAR_PROVIDER_URL):
        return True
    return False
