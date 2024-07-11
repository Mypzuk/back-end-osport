from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud

from .schemas import WhitelistIn, CheckWhitelist

from core.models import db_helper

from api.competitions.crud import get_competition



async def check_whitelist(whitelist_in: WhitelistIn, session: AsyncSession = Depends(db_helper.session_getter)):
    whitelist_user = await crud.get_whitelist_user(session=session, whitelist_in = whitelist_in)
    
    competition = await get_competition(session=session, competition_id = whitelist_in.competition_id)

    if competition is None: 
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Соревнования {whitelist_in.competition_id} не существует!",
    )

    if whitelist_user is not None: 
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Пользователь уже есть в вайтлисте",
    )

    return whitelist_in




