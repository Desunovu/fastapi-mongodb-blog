import os

from dotenv import load_dotenv

# Загрузка переменных окружения из файла .envexample
# без перезаписи если они уже существуют
dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.envexample'
)
load_dotenv_result = load_dotenv(dotenv_path=dotenv_path)

# Определение констант из переменных окружения
MONGODB_URL = os.getenv("MONGODB_URL", "")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
