# Функция создания базовых тестовых пользователей с ролями Admin, Author, Reader
import logging
from datetime import datetime

from ..core.security.roles import RolesEnum
from ..core.security.utilities import get_password_hash
from ..modules.users.models import UserDocument

# Add logger
log = logging.getLogger(__name__)


async def create_test_users():
    """Создает базовых тестовых пользователей"""

    test_users = [
        {
            "id": "65197008113d7dfdf95846f1",
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin",
            "role": RolesEnum.ADMIN.value,
        },
        {
            "id": "65197008113d7dfdf95846f2",
            "username": "author",
            "email": "author@example.com",
            "password": "author",
            "role": RolesEnum.AUTHOR.value,
        },
        {
            "id": "65197008113d7dfdf95846f3",
            "username": "reader",
            "email": "reader@example.com",
            "password": "reader",
            "role": RolesEnum.READER.value,
        },
    ]

    for user_data in test_users:
        # Проверка на наличие тестовых пользователей
        user_id_exists = await UserDocument.get(document_id=user_data["id"])
        if user_id_exists:
            continue
        user_name_exists = await UserDocument.find_one(
            UserDocument.username == user_data["username"]
        )
        if user_name_exists:
            log.warning(
                f"Тестовый пользователь {user_data['username']} уже существует c id {user_name_exists.id}"
            )
            continue

        # Создание документа
        user = UserDocument(
            id=user_data["id"],
            username=user_data["username"],
            password_hash=get_password_hash(user_data["password"]),
            email=user_data["email"],
            role=user_data["role"],
            created_at=datetime.utcnow(),
        )

        # Вставка документа
        await UserDocument.insert_one(user)

        log.info(f"Тестовый пользователь {user_data['username']} создан")
