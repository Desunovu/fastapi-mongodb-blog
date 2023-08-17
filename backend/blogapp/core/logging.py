from logging.config import dictConfig

from pydantic import BaseModel

from .config import LOGS_DIR_PATH, LOG_FILE_PATH, LOGGING_LEVEL, LOG_FORMAT, LOGGER_NAME


# From https://stackoverflow.com/questions/63510041/adding-python-logging-to-fastapi-endpoints-hosted-on-docker-doesnt-display-api
class LogConfig(BaseModel):
    """Конфигурация логгера"""

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": LOG_FILE_PATH,
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["file"], "level": LOGGING_LEVEL},
    }


def init_loggers():
    if not LOGS_DIR_PATH.exists():
        LOGS_DIR_PATH.mkdir()

    dictConfig(LogConfig().model_dump())
