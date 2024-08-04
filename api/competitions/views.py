from core.models import db_helper


from . import crud

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse

from .schemas import Competition, CompetitionCreate, CompetitionUpdate

from .dependencies import competition_check_by_type, competition_by_id
from api.users.schemas import UserLogin
from api.auth.dependencies import get_current_user

router = APIRouter(tags=["Competitions"])


@router.get("/")
async def get_competitions(
        check_auth: UserLogin = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.get_competitions(session=session)


@router.post("/")
async def create_competition(
    # /*= Depends(competition_check_by_type), */

    competition_in: CompetitionCreate,
        session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.create_competition(session=session, competition_in=competition_in)


@router.post('/create-manuals')
async def create_manuals(
    video: UploadFile = File(...),
):
    return await crud.create_manuals(video=video)


@ router.get("/{competition_id}")
async def get_competition(
    competition: Competition = Depends(competition_by_id),
    check_auth: UserLogin = Depends(get_current_user)

):
    return competition


@ router.delete("/{competition_id}")
async def delete_competition(
        competition: Competition = Depends(competition_by_id),
        session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.delete_competition(session=session, competition=competition)


@ router.put("/{competition_id}")
async def competition_update(
    competition_update: CompetitionUpdate,
    competition: Competition = Depends(competition_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud.competition_update(session=session, competition=competition, competition_update=competition_update)


@ router.post("/manuals/{competition_id}")
async def get_manual(competition: Competition = Depends(competition_by_id)):
    return StreamingResponse(crud.iterfile(competition=competition), media_type="video/quicktime")


# @router.get("/first")
# async def get_first_id(session: AsyncSession = Depends(db_helper.session_getter)):
#     return await crud.get_first_id(session=session)
