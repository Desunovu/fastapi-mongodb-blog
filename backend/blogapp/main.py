import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import FASTAPI_CREATE_TEST_USERS, FASTAPI_CHATGPT_API_KEY, \
    FASTAPI_CHATGPT_ALTERNATIVE_BASE
from .core.database.mongodb import init_odm
from .core.logging import init_loggers
from .core.security.routes import router as security_router
from .modules.articles.routes import router as articles_router
from .modules.comments.routes import router as comments_router
from .modules.gpt_writer.routes import router as gpt_writer_router
from .modules.gpt_writer.writer import Writer
from .modules.users.routes import router as users_router
from .utils.create_users import create_test_users

init_loggers()

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log = logging.getLogger("blogapp")


@app.on_event("startup")
async def startup():
    await init_odm()
    log.info("Инициализация ODM завершена")

    if FASTAPI_CREATE_TEST_USERS == "True":
        await create_test_users()
        log.info("Проверка тестовых пользователей завершена")

    if FASTAPI_CHATGPT_API_KEY:
        Writer.init_writer(FASTAPI_CHATGPT_ALTERNATIVE_BASE, FASTAPI_CHATGPT_API_KEY)
        log.info("Инициализация GPT API завершена")

    log.info("Выполнены подготовительные задачи при старте FastAPI")


# Подключить роутеры
routers = [
    security_router,
    articles_router,
    comments_router,
    users_router,
    gpt_writer_router,
]

for router in routers:
    app.include_router(router)
