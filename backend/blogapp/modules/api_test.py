from typing import Annotated

from fastapi import APIRouter, Depends

from .tags.model import TagDocument
from .users.model import UserDocument, UserBaseModel
from ..core.security.roles import RolesEnum
from ..core.security.utilities import RoleChecker

router = APIRouter(prefix="/test")


@router.get("/users/me")
async def test_users(
    current_user: Annotated[UserDocument, Depends(RoleChecker(RolesEnum.READER.value))]
):
    return UserBaseModel(**current_user.dict())


@router.post("/add_some_documents")
async def add_some_documents(
    current_user: Annotated[UserDocument, Depends(RoleChecker(RolesEnum.ADMIN.value))]
):
    tag = TagDocument(name="New tag")
    await TagDocument.insert_one(tag)

    return tag
