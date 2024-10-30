from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union
from core.models import db_helper

from .schemas import ResultCreate, ResultUpdate, ResultDenied
from . import crud

from api.competitions.crud import get_competition
from api.users.crud import get_user

from .crud import get_user_result_by_competition

from fastapi import Depends, HTTPException, status


async def result_by_id(
        result_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)):

    result = await crud.get_result(session=session, result_id=result_id)

    if result is not None:
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Результат {result_id} не найден!",
    )


async def check_result(
        result_id: int,
        result_in: ResultUpdate,
        session: AsyncSession = Depends(db_helper.session_getter)):

    result = await result_by_id(session=session, result_id=result_id)

    if result.count > result_in.count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Результат меньше предыдущего!",
        )

    return result_in


async def calc_points(result_in, competition):

    result_in.points = result_in.count * competition.coefficient

    return result_in


async def check_user_and_competition_and_result(
        result_in: ResultCreate,
        session: AsyncSession = Depends(db_helper.session_getter)):
    competition = await get_competition(session=session, competition_id=result_in.competition_id)
    if competition is None:
        raise HTTPException(
            status_code=400, detail="Соревнования не существует")

    user = await get_user(session=session, id=result_in.user_id)

    result = await get_user_result_by_competition(session=session, user=user, competition=competition)

    if result:
        if result.count >= result_in.count:
            raise HTTPException(
                status_code=200, detail="Результат не больше предыдущего")

    return await calc_points(result_in, competition)


async def check_user_and_competition_and_result1(
        result_in: ResultDenied,
        session: AsyncSession = Depends(db_helper.session_getter)):

    competition = await get_competition(session=session, competition_id=result_in.competition_id)

    if competition is None:
        raise HTTPException(
            status_code=400, detail="Соревнования не существует")

    user = await get_user(session=session, id=result_in.user_id)

    if user is None:
        raise HTTPException(
            status_code=400, detail="Пользователя не существует")

    if user is None:
        raise HTTPException(
            status_code=400, detail="Пользователя не существует")

    return await calc_points(result_in, competition)
