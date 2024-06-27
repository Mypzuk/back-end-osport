from core.models import db_helper

from . import crud 

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Competition, CompetitionCreate, CompetitionUpdate

from .dependencies import competition_check_by_type, competition_by_id

router = APIRouter(tags=["Competitions"])



@router.get("/")
async def get_competitions(session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.get_competitions(session=session)



@router.post("/")
async def create_competition(
    competition_in: CompetitionCreate = Depends(competition_check_by_type),
    session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.create_competition(session=session, competition_in=competition_in)


@router.get("/{competition_id}")
async def get_competition(
    competition: Competition = Depends(competition_by_id)
):
    return competition


@router.delete("/{competition_id}")
async def delete_competition(
    competition: Competition = Depends(competition_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.delete_competition(session=session, competition=competition)




@router.put("/{competition_id}")
async def competition_update(
    competition_update: CompetitionUpdate,
    competition: Competition = Depends(competition_by_id), 
    session: AsyncSession = Depends(db_helper.session_getter)
): 
    return await crud.competition_update(session=session, competition=competition, competition_update=competition_update)



@router.get("/first")
async def get_first_id(session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.get_first_id(session=session)