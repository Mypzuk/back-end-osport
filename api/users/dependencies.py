from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from . import crud

from .schemas import UserCreate, UserLogin


async def user_by_id(user_id: Annotated[int, Path],session: AsyncSession = Depends(db_helper.session_getter),):
    user = await crud.get_user(session=session, id=user_id)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )




async def user_check_by_login(user_create: UserCreate, session: AsyncSession = Depends(db_helper.session_getter), ):
    user = await crud.get_user(session=session, login=user_create.login)
    if user is not None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User login already exsist",
    )
    return user_create



async def user_login_check(user_login: UserLogin, session: AsyncSession = Depends(db_helper.session_getter), ):
    user = await crud.get_user(session=session, login=user_login.login)
    if user is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User login not found",
    )
    return user_login