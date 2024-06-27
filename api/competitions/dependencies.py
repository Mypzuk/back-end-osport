from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from .schemas import CompetitionCreate
from . import crud


from fastapi import Depends, HTTPException, status




async def competition_by_id(
    competition_id: int, 
    session: AsyncSession = Depends(db_helper.session_getter)):

    competition = await crud.get_competition(session=session, competition_id=competition_id)
    if competition is not None: 
        return competition
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Competition {competition_id} not found!",
    )





async def competition_check_by_type(
        competition_create: CompetitionCreate,
        session: AsyncSession = Depends(db_helper.session_getter)):
    
    competition = await crud.get_competition(session=session, type=competition_create.type) 
    if competition is not None: 
        raise HTTPException(status_code=400, detail="Соревнование уже существует")
    return competition_create