from fastapi import APIRouter

from .tags.model import Tag

router = APIRouter(
    prefix="/test"
)


@router.post("/add_some_documents")
async def add_some_documents():
    tag = Tag(name="New tag")
    await Tag.insert_one(tag)

    return tag
