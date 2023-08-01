from typing import Annotated

from fastapi import APIRouter, Depends

from .tags.model import Tag
from ..core.oauth import oauth2_scheme

router = APIRouter(
    prefix="/test"
)


@router.get("/test_token/")
async def test_token(token: Annotated[str, Depends(oauth2_scheme)]):

    return {"token": token}


@router.post("/add_some_documents")
async def add_some_documents():
    tag = Tag(name="New tag")
    await Tag.insert_one(tag)

    return tag
