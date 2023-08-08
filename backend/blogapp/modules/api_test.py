from typing import Annotated

from fastapi import APIRouter, Depends

from .users.model import UserBase
from ..core.security.roles import RolesEnum
from ..core.security.utilities import RoleChecker

router = APIRouter(prefix="/test")


@router.get("/users/me", response_model=UserBase)
async def test_users(
    current_user: Annotated[UserBase, Depends(RoleChecker(RolesEnum.READER.value))]
):
    return current_user
