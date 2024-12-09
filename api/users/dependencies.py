

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from . import crud

import bcrypt

from .schemas import UserCreate, UserLogin, UserPassword


async def user_by_id(user_id: int, session: AsyncSession = Depends(db_helper.session_getter),):
    user = await crud.get_user(session=session, id=user_id)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Пользователь {user_id} не найден!",
    )


async def user_check_by_email_and_login(user_create: UserCreate, session: AsyncSession = Depends(db_helper.session_getter), ):
    user = await crud.get_user(session=session, login=user_create.login)

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Такой логин уже существует",
        )

    user = await crud.get_user(session=session, email=user_create.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Такой email уже существует",
        )

    return user_create


async def user_login_check(user_login: UserLogin, session: AsyncSession = Depends(db_helper.session_getter), ):
    user = await crud.get_user(session=session, login=user_login.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Логин не найден",
        )

    return await user_password_check(user=user, user_password=user_login)


async def user_password_check(user, user_password):
    is_valid = await unhash_password(user_password.password, user.password)
    if is_valid:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Неправильный пароль",
    )

async def hash_password(password: str) -> str:
    # Хэшируем пароль и возвращаем как строку
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Сохраняем хэш в базе данных как строку


async def unhash_password(password: str, hashed_password: str) -> bool:
    # Конвертируем строку из базы обратно в байты
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    # Проверяем пароль с хэшом
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)