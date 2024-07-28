from core.models import db_helper
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from .schemas import WhitelistIn, CheckWhitelist

from .dependencies import check_whitelist

from . import crud

from api.users.schemas import UserLogin
from api.auth.dependencies import get_current_user


router = APIRouter(tags=["Whitelist"])


@router.post("/")
async def create_whitelist_user(
        whitelist_in: WhitelistIn = Depends(check_whitelist),
        session: AsyncSession = Depends(db_helper.session_getter),
        check_auth: UserLogin = Depends(get_current_user)):

    return await crud.create_whitelist_user(session=session, whitelist_in=whitelist_in)


@router.get("/")
async def get_whitelist_users(session: AsyncSession = Depends(db_helper.session_getter), check_auth: UserLogin = Depends(get_current_user)):
    return await crud.get_whitelist_users(session=session)


@router.post("/check")
async def get_whitelist_user_by_id(
        whitelist_in: CheckWhitelist,
        session: AsyncSession = Depends(db_helper.session_getter),
        check_auth: UserLogin = Depends(get_current_user)):

    return await crud.get_whitelist_user_by_id(whitelist_in=whitelist_in, session=session)
