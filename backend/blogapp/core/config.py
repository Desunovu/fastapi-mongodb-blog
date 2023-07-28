import os

from dotenv import load_dotenv

# Загрузка переменных окружения из файла .envexample
# без перезаписи если они уже существуют
dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.envexample'
)
load_dotenv(dotenv_path=dotenv_path)
