from typing import Annotated

from fastapi import APIRouter, Depends

from .tags.model import Tag
from .users.model import User
from ..core.security.utilities import get_active_current_user

router = APIRouter(
    prefix="/test"
)


@router.get("/users/me")
async def test_users(
    current_user: Annotated[User, Depends(get_active_current_user)]
):
    return current_user


@router.post("/add_some_documents")
async def add_some_documents():
    tag = Tag(name="New tag")
    await Tag.insert_one(tag)

    return tag
