from typing import Annotated

from fastapi import APIRouter, Depends

from .users.models import UserDocument
from ..core.security.roles import RolesEnum
from ..core.security.utilities import RoleChecker

router = APIRouter(prefix="/test")


@router.get("/users/me")
async def test_users(
    current_user: Annotated[UserDocument, Depends(RoleChecker(RolesEnum.READER.value))]
):
    return current_user
