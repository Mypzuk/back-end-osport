
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Results"])

from core.models import db_helper

from . import crud

from .schemas import Result, ResultCreate, ResultUpdate

from api.competitions.schemas import Competition
from api.competitions.dependencies import competition_by_id

from api.users.schemas import User
from api.users.dependencies import user_by_id

from .dependencies import check_result, result_by_id, check_user_and_competition_and_result




@router.get("/")
async def get_results(session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.get_results(session=session)





@router.post("/")
async def create_result(
    result_in: ResultCreate = Depends(check_user_and_competition_and_result),
    session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.create_result(session=session, result_in=result_in)
    


@router.put("/{result_id}")
async def update_result(
    result_update: ResultUpdate = Depends(check_result),
    result: Result = Depends(result_by_id), 
    session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.update_result(session=session, result=result, result_update=result_update)
 



@router.delete("/{result_id}")
async def delete_result(
    result: Result = Depends(result_by_id), 
    session: AsyncSession = Depends(db_helper.session_getter)):
    
    return await crud.delete_result(session=session, result=result)





@router.post("/{result_id}/nulify")
async def nulify_result(
    result: Result = Depends(result_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.nulify_result(session=session, result=result)
    



@router.get("/user/{user_id}")
async def get_user_results(
    user: User = Depends(user_by_id), 
    session: AsyncSession = Depends(db_helper.session_getter)):
    
    return await crud.get_user_results(session=session, user=user)




@router.get("/user/{user_id}/commpetition/{competition_id}")
async def get_user_result_by_competition(
    user: User = Depends(user_by_id),
    competition: Competition = Depends(competition_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud.get_user_result_by_competition(session=session, user=user, competition=competition)



@router.get("/commpetition/{competition_id}")
async def get_competition_result(
    competition: Competition = Depends(competition_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.get_competition_result(session=session,competition=competition)




@router.get("/commpetition/{competition_id}/participants")
async def get_competition_participants(
    competition: Competition = Depends(competition_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.get_competition_participants(session=session,competition=competition)


@router.get("/commpetition/{competition_id}/user/{user_id}/status")
async def check_user_status_by_competition(
    competition: Competition = Depends(competition_by_id),
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.check_user_status_by_competition(session=session, user=user, competition=competition)



@router.get("/commpetition/{competition_id}/rating")
async def get_competition_rating(
    competition: Competition = Depends(competition_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.get_competition_rating(session=session,competition=competition)




@router.get("/rating")
async def get_total_rating(session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.get_total_rating(session=session)




@router.get("/user/{user_id}/competitions")
async def competition_info(
    user: User = Depends (user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.competition_info(session=session, user=user)