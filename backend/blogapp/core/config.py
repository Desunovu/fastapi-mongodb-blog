import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv

log = logging.getLogger("blogapp")

mode = os.getenv("FASTAPI_APP_MODE", "DEV")
if mode == "DEV":
    # Загрузка переменных окружения из файла ".env.development.example в /backend"
    # Не перезаписывает уже заданные переменные.
    # Переменные для prod устанавливаются в docker-compose.yml
    env_path = os.path.join(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        ),
        ".env.development",
    )
    log.debug(f"[DEV MODE] Путь к файлу .env: {env_path}")
    load_dotenv_result = load_dotenv(dotenv_path=env_path)
elif mode == "PROD":
    log.debug(f"[PROD MODE]")

# Получение переменных окружения приложения
FASTAPI_SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY", "")

FASTAPI_CHATGPT_ALTERNATIVE_BASE = os.getenv("FASTAPI_CHATGPT_ALTERNATIVE_BASE", "")
FASTAPI_CHATGPT_API_KEY = os.getenv("FASTAPI_CHATGPT_API_KEY", "")

FASTAPI_CREATE_TEST_USERS = os.getenv("FASTAPI_CREATE_TEST_USERS", "DEV")
FASTAPI_LOGGING_LEVEL = os.getenv("FASTAPI_LOGGING_LEVEL", "DEBUG")
FASTAPI_MONGODB_URL = os.getenv("FASTAPI_MONGODB_URL", "")
FASTAPI_MONGODB_DATABASE = os.getenv("FASTAPI_MONGODB_DATABASE", "")

# Прочие константы
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600

# Вычисление абсолютных путей приложения
BACKEND_DIR_PATH: Path = Path().parent.parent.absolute()

# LOGGER
LOGGER_NAME: str = "blogapp"
LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
LOGS_DIR_PATH: Path = BACKEND_DIR_PATH / "logs"
LOG_FILE_PATH: Path = LOGS_DIR_PATH / f"""{time.strftime("%Y%m%d-%H%M%S")}.log"""

# Аватары пользователей
DEFAULT_AVATAR_URL: str = "https://cdn-icons-png.flaticon.com/512/149/149071.png"
AVATAR_PROVIDER_URL: str = "https://cdn-icons-png.flaticon.com"

# Параметры статей
ARTICLE_MAX_LENGTH: int = 10000
