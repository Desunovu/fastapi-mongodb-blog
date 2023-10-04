import os
import time
from pathlib import Path

from dotenv import load_dotenv

mode = os.getenv("APP_MODE", "development")
if mode == "development":
    # Загрузка переменных окружения из файла ".env.development в /backend"
    # Не перезаписывает уже заданные переменные.
    # Переменные для prod устанавливаются в docker-compose.yml
    env_path = os.path.join(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        ),
        ".env.development",
    )
    print(f"[DEV MODE] Путь к файлу .env: {env_path}")
    load_dotenv_result = load_dotenv(dotenv_path=env_path)
elif mode == "production":
    print(f"[PROD MODE]")

# Определение констант приложения
SECRET_KEY = os.getenv("SECRET_KEY", "")
FASTAPI_CREATE_TEST_USERS = os.getenv("FASTAPI_CREATE_TEST_USERS", "DEV")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "DEBUG")
MONGODB_URL = os.getenv("MONGODB_URL", "")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "")

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
