from . import crud
from fastapi import APIRouter, Depends
from .schemas import Token

from api.users.dependencies import user_login_check
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.models import db_helper

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter)

):
    user = await user_login_check(form_data, session)
    return await crud.login(user=user)


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    return await crud.refresh_token(refresh_token=refresh_token)
