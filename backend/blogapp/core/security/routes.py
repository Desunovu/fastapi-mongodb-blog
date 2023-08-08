from datetime import datetime
from typing import Annotated

from beanie.odm.operators.find.comparison import Eq
from beanie.odm.operators.find.logical import Or
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from .schema import TokenResponseBody, RegisterRequestBody
from .utilities import authenticate_user, create_access_token, get_password_hash
from ...modules.users.model import UserDocument

router = APIRouter()


@router.post("/token", response_model=TokenResponseBody)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Выдает токен доступа аутентифицированному пользователю"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserDocument)
async def register_user(body: RegisterRequestBody):
    """Создает нового пользователя"""
    # Проверить не занят ли username и email
    existing_user = await UserDocument.find(
        Or(Eq(UserDocument.email, body.email), Eq(UserDocument.username, body.username))
    ).first_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    user = UserDocument(
        username=body.username,
        password_hash=get_password_hash(body.password),
        email=body.email,
        disabled=False,
        created_at=datetime.utcnow(),
    )
    await UserDocument.insert_one(user)
    return user
