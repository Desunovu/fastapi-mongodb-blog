from typing import Annotated

from beanie import PydanticObjectId
from beanie.odm.enums import SortDirection
from fastapi import APIRouter, Depends, Query, Path, HTTPException, Body
from starlette import status

from .models import (
    UserDocument,
    UsersResponse,
    UsersSortField,
    UserResponse,
    UpdateUserRequest,
    UpdateUserPasswordRequest,
)
from ...core.security.roles import RolesEnum
from ...core.security.utilities import (
    RoleChecker,
    get_active_current_user,
    verify_password,
    get_password_hash,
)

router = APIRouter(prefix="/users")


@router.get("/", response_model=UsersResponse)
async def list_users(
    _current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    skip: Annotated[int | None, Query(ge=0)] = None,  # >= 0
    limit: Annotated[int | None, Query(ge=1)] = None,  # >= 1
    sort_by: Annotated[UsersSortField, Query()] = UsersSortField.created_at.value,
    sort_order: Annotated[SortDirection, Query()] = SortDirection.DESCENDING.value,
):
    """Возвращает список пользователей"""

    # Базовый запрос
    query = UserDocument.find(fetch_links=True)
    # Сортировка, пагинация
    query = query.sort((sort_by, sort_order)).skip(n=skip).limit(n=limit)
    # Получение списка пользователей
    users = await query.to_list(length=None)

    return {"users": users}


@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: Annotated[UserDocument, Depends(get_active_current_user)],
):
    """Возвращает текущего пользователя"""

    return {"user": current_user}


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    _current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    user_id: Annotated[PydanticObjectId, Path(description="UUID Пользователя")],
):
    """Возвращает пользователя по id"""

    user = await UserDocument.get_or_404(document_id=user_id)

    return {"user": user}


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    user_id: Annotated[PydanticObjectId, Path(description="UUID Пользователя")],
    user_data: UpdateUserRequest,
):
    """Обновляет пользователя по id"""

    user = await UserDocument.update_document_by_id(
        document_id=user_id,
        current_user=current_user,
        update_data=user_data,
    )

    return {"user": user}


@router.put("/{user_id}/password")
async def update_user_password(
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    user_id: Annotated[PydanticObjectId, Path(description="UUID Пользователя")],
    password_data: UpdateUserPasswordRequest,
):
    """Обновляет пароль пользователя по id"""

    user = await UserDocument.get_or_404(document_id=user_id)
    user.check_user_can_modify_document(current_user)
    # Проверки если обновляется профиль текущего пользователя
    if user.id == current_user.id:
        # Сверить old_password
        if not verify_password(
            plain_password=password_data.old_password,
            hashed_password=current_user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный пароль",
            )
    # Если обновляем не свой аккаунт
    else:
        # Запретить менять пароль другим администраторам
        if user.role == RolesEnum.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нельзя изменить пароль другому администратору",
            )
    # Записать новый пароль
    user.password_hash = get_password_hash(password_data.new_password)
    await user.save()

    return {"message": "Пароль обновлен"}


@router.put("/{user_id}/disable")
async def disable_user(
    _current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.ADMIN.value))
    ],
    user_id: str = Path(description="UUID пользователя"),
):
    """Заблокировать пользователя по id [АДМИНИСТРАТОР]"""

    user = await UserDocument.get_or_404(document_id=user_id)
    # Запретить блокировать администраторов
    if user.role == RolesEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя заблокировать администратора",
        )
    # Заблокировать пользователя
    user.disabled = True
    await user.save()

    return {"message": "Пользователь успешно отключен"}


@router.put("/{user_id}/role")
async def change_user_role(
    _current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.ADMIN.value))
    ],
    user_id: Annotated[str, Path(description="UUID пользователя")],
    role: Annotated[RolesEnum, Body(embed=True, description="Роль")],
):
    """Изменить роль пользователя по id [АДМИНИСТРАТОР]"""

    user = await UserDocument.get_or_404(document_id=user_id)
    # Запретить назначать администраторов
    if role == RolesEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя назначить роль администратора",
        )
    # Запретить изменять роль администраторов
    if user.role == RolesEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя менять роль администратора",
        )
    # Изменить роль
    user.role = role
    await user.save()

    return {"message": f"Пользователю назначена роль {role.value}"}
