import logging

from fastapi import FastAPI

from .core.database.mongodb import init_odm
from .core.logging import init_loggers
from .core.security import routes as security_routes
from .modules.articles.routes import router as articles_router
from .modules.comments.routes import router as comments_router
from .modules.users.routes import router as users_router

init_loggers()

app = FastAPI()

log = logging.getLogger("blogapp")


@app.on_event("startup")
async def startup():
    await init_odm()
    log.info("Выполнены задачи startup event'а")


app.include_router(security_routes.router)
app.include_router(articles_router)
app.include_router(comments_router)
app.include_router(users_router)
