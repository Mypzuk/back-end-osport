from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud

from api.users.schemas import UserLogin
from api.auth.dependencies import get_current_user


from .schemas import User, UserCreate, UserUpdateBirthday, UserLogin, UserUpdate, UserPassword, NewUserPass, UserUpdateAfterCreate

from core.models import db_helper

from .dependencies import user_by_id, user_check_by_email_and_login, user_login_check

router = APIRouter(tags=["Users"])


@router.get("/")
async def get_users(session: AsyncSession = Depends(db_helper.session_getter), check_auth: UserLogin = Depends(get_current_user)):
    return await crud.get_users(session=session)


@router.post("/", status_code=status.HTTP_201_CREATED,)
async def create_user(
        user_in: UserCreate = Depends(user_check_by_email_and_login),
        session: AsyncSession = Depends(db_helper.session_getter),):

    return await crud.create_user(session=session, user_in=user_in)


@router.patch("/{user_id}")
async def patch_user_after_registration(
    user_in: UserUpdateAfterCreate,
        check_auth: UserLogin = Depends(get_current_user),
        user: User = Depends(user_by_id),
        session: AsyncSession = Depends(db_helper.session_getter)):

    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")

    return await crud.patch_user_after_registration(session=session, user=user, user_in=user_in)


# @router.post("/login")
# async def user_login(
#     user: UserLogin = Depends(user_login_check),
#     session: AsyncSession = Depends(db_helper.session_getter),):

#     return await crud.user_login(user=user)


@router.get("/{user_id}/")
async def get_user(user: User = Depends(user_by_id), check_auth: UserLogin = Depends(get_current_user)):
    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")
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
    check_auth: UserLogin = Depends(get_current_user),
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")
    return await crud.update_user_birthdate(session=session, user=user, user_update=user_update)


@router.patch("/{user_id}/height-weight")
async def update_user_data(
    user_update: UserUpdate,
    user: User = Depends(user_by_id),
    check_auth: UserLogin = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")
    return await crud.update_user_data(session=session, user=user, user_update=user_update)


@router.post("/{user_id}/check-password")
async def check_user_password(
    user_password: UserPassword,
    user: User = Depends(user_by_id),
    check_auth: UserLogin = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")
    return await crud.check_user_password(session=session, user=user, user_password=user_password)


@router.patch("/{user_id}/change-password")
async def change_user_password(
    user_password: NewUserPass,
    user: User = Depends(user_by_id),
    check_auth: UserLogin = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")
    return await crud.change_user_password(session=session, user=user, user_password=user_password)


@router.get("/profile")
async def user_profile(
    user: User = Depends(user_by_id),
    check_auth: UserLogin = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter)

):
    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")
    return await crud.user_profile(session=session, user=user)
