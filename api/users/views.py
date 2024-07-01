from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud 


from .schemas import User, UserCreate, UserUpdateBirthday, UserLogin, UserUpdate, UserPassword, NewUserPass

from core.models import db_helper

from .dependencies import user_by_id, user_check_by_login, user_login_check

router = APIRouter(tags=["Users"])


@router.get("/")
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.get_users(session=session)




@router.post("/", status_code=status.HTTP_201_CREATED,)
async def create_user(
    user_in: UserCreate = Depends(user_check_by_login),
    session: AsyncSession = Depends(db_helper.session_getter),):

    return await crud.create_user(session=session, user_in=user_in)





@router.post("/login")
async def user_login(
    user: UserLogin = Depends(user_login_check),
    session: AsyncSession = Depends(db_helper.session_getter),):

    return await crud.user_login()



@router.get("/{user_id}/")
async def get_user(user: User = Depends(user_by_id),):
    return user



@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user: User = Depends(user_by_id), 
    session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud.delete_user(session=session, user=user)
    


@router.patch("/{user_id}/birthdate", response_model=dict)
async def update_user_birthdate(
    user_update: UserUpdateBirthday,
    user: User = Depends(user_by_id), 
    session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud.update_user_birthdate(session=session, user=user, user_update=user_update)
    


@router.patch("/{user_id}/height-weight")
async def update_user_data(
    user_update: UserUpdate,
    user: User = Depends(user_by_id), 
    session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud.update_user_data(session=session, user=user, user_update=user_update)




@router.patch("/{user_id}/check-password")
async def check_user_password( 
    user_password: UserPassword,
    user: User = Depends(user_by_id), 
    session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud.check_user_password(session=session, user=user, user_password=user_password)




@router.patch("/{user_id}/change-password")
async def change_user_password( 
    user_password: NewUserPass,
    user: User = Depends(user_by_id), 
    session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud.change_user_password(session=session, user=user, user_password=user_password)