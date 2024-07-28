
from api.users.schemas import UserLogin
from api.auth.dependencies import get_current_user
from .dependencies import check_result, result_by_id, check_user_and_competition_and_result, check_user_and_competition_and_result1
from api.users.dependencies import user_by_id
from api.users.schemas import User
from api.competitions.dependencies import competition_by_id
from api.competitions.schemas import Competition
from .schemas import Result, ResultCreate, ResultUpdate, ResultDenied
from . import crud
from core.models import db_helper
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Results"])


@router.get("/")
async def get_results(session: AsyncSession = Depends(db_helper.session_getter), check_auth: UserLogin = Depends(get_current_user)):
    return await crud.get_results(session=session)


@router.post("/")
async def create_result(
        result_in: ResultCreate = Depends(
            check_user_and_competition_and_result),
        check_auth: UserLogin = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.create_result(session=session, result_in=result_in)


@router.post("/denied-result")
async def denied_result(
        new_count: int,
        result_in: ResultDenied = Depends(
            check_user_and_competition_and_result1),
        check_auth: UserLogin = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.create_result(session=session, result_in=result_in)



# @router.put("/{result_id}")
# async def update_result(
#     result_update: ResultUpdate = Depends(check_result),
#     result: Result = Depends(result_by_id), 
#     session: AsyncSession = Depends(db_helper.session_getter)):

#     return await crud.update_result(session=session, result=result, result_update=result_update)
 



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
        check_auth: UserLogin = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)):

    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")

    return await crud.get_user_results(session=session, user=user)


@router.get("/user/{user_id}/commpetition/{competition_id}")
async def get_user_result_by_competition(
    user: User = Depends(user_by_id),
    check_auth: UserLogin = Depends(get_current_user),
    competition: Competition = Depends(competition_by_id),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")
    return await crud.get_user_result_by_competition(session=session, user=user, competition=competition)


@router.get("/commpetition/{competition_id}")
async def get_competition_result(
        competition: Competition = Depends(competition_by_id),
        session: AsyncSession = Depends(db_helper.session_getter),
        check_auth: UserLogin = Depends(get_current_user)):

    return await crud.get_competition_result(session=session, competition=competition)


@router.get("/commpetition/{competition_id}/participants")
async def get_competition_participants(
        competition: Competition = Depends(competition_by_id),
        check_auth: UserLogin = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.get_competition_participants(session=session, competition=competition)


@router.get("/commpetition/{competition_id}/user/{user_id}/status")
async def check_user_status_by_competition(
        competition: Competition = Depends(competition_by_id),
        check_auth: UserLogin = Depends(get_current_user),
        user: User = Depends(user_by_id),
        session: AsyncSession = Depends(db_helper.session_getter)):
    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")
    return await crud.check_user_status_by_competition(session=session, user=user, competition=competition)


@router.get("/commpetition/{competition_id}/rating")
async def get_competition_rating(
        competition: Competition = Depends(competition_by_id),
        check_auth: UserLogin = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)):

    return await crud.get_competition_rating(session=session, competition=competition)


@router.get("/rating")
async def get_total_rating(session: AsyncSession = Depends(db_helper.session_getter), check_auth: UserLogin = Depends(get_current_user)):

    return await crud.get_total_rating(session=session)


@router.get("/user/{user_id}/competitions")
async def competition_info(
        user: User = Depends(user_by_id),
        check_auth: UserLogin = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)):
    if user.id != check_auth.user_id:
        raise HTTPException(
            status_code=403, detail="Отказано в доступе: У вас нет доступа к этому ресурсу")
    return await crud.competition_info(session=session, user=user)
