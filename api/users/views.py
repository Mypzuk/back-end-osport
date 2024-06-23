from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud 

from .schemas import User, UserCreate

from core.models import db_helper

from .dependencies import user_by_id

router = APIRouter(tags=["Users"])


@router.get("/")
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.get_users(session=session)


@router.post("/", status_code=status.HTTP_201_CREATED,)
async def create_user(user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_getter),):
    return await crud.create_user(session=session, user_in=user_in)



@router.get("/{user_id}/")
async def get_user(user: User = Depends(user_by_id),):
    return user



# @router.patch("/{user_id}/birthdate")
# async def update_bithdate(user_in: ):
