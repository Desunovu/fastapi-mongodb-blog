import os

from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

# Определение констант из переменных окружения
MONGODB_URL = os.environ.get("MONGODB_URL")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE")

# Motor client
mongo_client = AsyncIOMotorClient(MONGODB_URL)


# Возвращение клиента с указанием нужной базы
def get_mongodb_client(request: Request) -> AsyncIOMotorClient:
    print(MONGODB_DATABASE, MONGODB_URL)
    return request.app.state.mongo_client[MONGODB_DATABASE]
