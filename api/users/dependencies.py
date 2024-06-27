from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from . import crud

from .schemas import UserCreate


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
        return "uzhe"
    return user_create