from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from .schemas import ResultCreate, ResultUpdate
from . import crud

from api.competitions.crud import get_competition 
from api.users.crud import get_user


from fastapi import Depends, HTTPException, status



async def result_by_id(
    result_id: int, 
    session: AsyncSession = Depends(db_helper.session_getter)):

    result = await crud.get_result(session=session, result_id=result_id)
    if result is not None:
        return result 
    

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Result {result_id} not found!",
    )



async def check_user_and_competition(
    result_in: ResultCreate | ResultUpdate,
    session: AsyncSession = Depends(db_helper.session_getter)):
    
    competition = await get_competition(session=session, competition_id=result_in.competition_id) 

    if competition is None: 
        raise HTTPException(status_code=400, detail="Соревнования не существует")
    
    user = await get_user(session=session, id=result_in.user_id) 
    if user is None: 
        raise HTTPException(status_code=400, detail="Пользователя не существует")
    
    
    return await calc_points(result_in, competition)
    


async def calc_points(result_in, competition) :

    result_in.points = result_in.count * competition.coefficient

    return result_in



