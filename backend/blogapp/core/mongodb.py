from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .config import MONGODB_URL, MONGODB_DATABASE
from ..modules.articles.model import Article
from ..modules.users.model import User
from ..modules.comments.model import Comment
from ..modules.tags.model import Tag


# Init beanie ODM
async def init_odm():
    mongo_client = AsyncIOMotorClient(MONGODB_URL)
    await init_beanie(
        database=mongo_client[MONGODB_DATABASE],
        document_models=[Article, User, Comment, Tag]
    )
