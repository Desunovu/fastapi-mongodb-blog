from datetime import timedelta, datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from .roles import RolesEnum
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from ...modules.users.model import UserDocument, UserBase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет совпадение пароля с хэшем"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Возвращает хэш пароля"""
    return pwd_context.hash(password)


async def get_user_by_username(username: str) -> UserDocument | None:
    """Получает пользователя из БД по username"""
    user = await UserDocument.find_one(UserDocument.username == username)
    return user


async def authenticate_user(username: str, password: str) -> UserDocument | None:
    """Аутентифицирует пользователя по username и password"""
    user = await get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создает токен доступа с данными из словаря"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserBase:
    """Зависимость - возвращает UserBase по переданному токену"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username)
    if not user:
        raise credentials_exception
    return UserBase.parse_obj(user.dict())


async def get_active_current_user(
    current_user: Annotated[UserBase, Depends(get_current_user)]
) -> UserBase:
    """Зависимость - возвращает активного пользователя"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class RoleChecker:
    """
    Класс зависимости обеспечения контроля доступа на основе ролей.
    Возвращает UserBase если проверка успешна
    """

    def __init__(self, allowed_role: str):
        self.allowed_role = allowed_role

    def __call__(
        self, current_user: Annotated[UserBase, Depends(get_active_current_user)]
    ) -> UserBase:
        allowed_role_value = RolesEnum.role_to_value(self.allowed_role)
        user_role_value = RolesEnum.role_to_value(current_user.role)
        if user_role_value < allowed_role_value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
            )

        return current_user
