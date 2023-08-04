from typing import Annotated

from fastapi import APIRouter, Depends

from .tags.model import TagDocument
from .users.model import UserDocument
from ..core.security.utilities import get_active_current_user

router = APIRouter(
    prefix="/test"
)


@router.get("/users/me")
async def test_users(
        current_user: Annotated[UserDocument, Depends(get_active_current_user)]
):
    return current_user


@router.post("/add_some_documents")
async def add_some_documents():
    tag = TagDocument(name="New tag")
    await TagDocument.insert_one(tag)

    return tag
