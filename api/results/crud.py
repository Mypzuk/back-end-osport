import os

from sqlalchemy import select, and_, desc, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Results, Competitions

from .schemas import Result, ResultCreate, ResultUpdate
from api.users.schemas import User
from api.competitions.schemas import Competition

from api.competitions.crud import get_competition
from api.users.crud import get_user

status_wait_adm = "wait_adm"

async def get_results(session: AsyncSession):
    stmt = select(Results).order_by(Results.competition_id)
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)

async def get_result(session: AsyncSession, **kwargs):
    query = select(Results)
    for key, value in kwargs.items():
        query = query.where(getattr(Results, key) == value)
    result = await session.execute(query)
    return result.scalars().first()

# ----- придумать как передавать необязательный параметр
async def create_result(session: AsyncSession, result_in):
    competition = await get_competition(session=session, competition_id=result_in.competition_id) 
    user = await get_user(session=session, id=result_in.user_id)
    
    result = await get_user_result_by_competition_special_for_denied_result(session=session, user=user, competition=competition)

    if result:
        if result.status == 'checked_cv':
            user.total_experience = (user.total_experience - result.points) - 20
            user.current_experience = (user.current_experience - result.points) - 20
            
        for name, value in result_in.model_dump().items():
            setattr(result, name, value)
        
        if result_in.status == 'checked_cv':
            try:
                os.remove(f"api/cv/cvmedia/{result_in.video}")
            except FileNotFoundError:
                return {"message": "Такого видео нет на сервере :c"}
            user.total_experience = (user.total_experience + result_in.points) + 20
            user.current_experience = (user.current_experience + result_in.points) + 20
    else:
        if result_in.status == 'checked_cv':
            user = await get_user(session=session, id=result_in.user_id)

            try:
                os.remove(f"api/cv/cvmedia/{result_in.video}")
            except FileNotFoundError:
                return {"message": "Такого видео нет на сервере :c"}

            user.total_experience = (user.total_experience + result_in.points) + 20
            user.current_experience = (user.current_experience + result_in.points) + 20 

        result = Results(**result_in.model_dump())
        session.add(result)
        
    await session.commit()
    await session.refresh(result)
    return result

async def update_result(session: AsyncSession, result: Result, result_update: ResultUpdate):
    competition = await get_competition(session=session, competition_id=result.competition_id)
    user = await get_user(session=session, id=result.user_id)

    setattr(user, "current_experience", user.current_experience + (result_update.count - result.count) * competition.coefficient)
    setattr(user, "total_experience", user.total_experience + (result_update.count - result.count) * competition.coefficient)
    
    setattr(result, "points", result_update.count * competition.coefficient)

    for name, value in result_update.model_dump().items():
        setattr(result, name, value)

    await session.commit()
    return result

async def delete_result(session: AsyncSession, result):
    await session.delete(result)
    await session.commit()
    return {"status": "Удачно", "message": "Результат успешно удален"}    

async def nulify_result(session: AsyncSession, result):
    stmt = select(Results).where(Results.result_id == result.result_id)
    result_obj = await session.execute(stmt)
    result_row = result_obj.scalar_one_or_none()

    result_row.count = 0 
    result_row.points = 0

    await session.commit()
    return result_row

async def get_user_results(session: AsyncSession, user: User):
    stmt = select(Results).where(and_(Results.user_id == user.id, Results.status != status_wait_adm))
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)

async def get_user_result_by_competition(session: AsyncSession, user, competition):
    stmt = select(Results).where(and_(Results.user_id == user.id, Results.competition_id == competition.competition_id, Results.status != status_wait_adm))
    result = await session.execute(stmt)
    data = result.scalars().first()
    return data

async def get_competition_result(session: AsyncSession, competition):
    stmt = select(Results).where(and_(Results.competition_id == competition.competition_id, Results.status != status_wait_adm))
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)

async def get_competition_participants(session: AsyncSession, competition):
    stmt = select(Results.user_id).where(and_(Results.competition_id == competition.competition_id, Results.status != status_wait_adm)).distinct()
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)

async def check_user_status_by_competition(session: AsyncSession, user, competition):
    stmt = select(Results.status).where(and_(Results.competition_id == competition.competition_id, Results.user_id == user.id))
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)

async def get_competition_rating(session: AsyncSession, competition):
    stmt = select(Results).where(and_(Results.competition_id == competition.competition_id, Results.status != status_wait_adm)).order_by(desc(Results.count))
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)

async def get_total_rating(session: AsyncSession):
    stmt = select(Results.user_id, func.sum(Results.points)).where(Results.status != status_wait_adm).filter(Results.status.isnot(None), Results.count > 0).group_by(Results.user_id).order_by(desc(func.sum(Results.points)))
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return data

async def competition_info(session: AsyncSession, user):
    competitions = await session.execute(
        select(
            Results.competition_id,
            Competitions.title,
            Results.count
        )
        .join(Competitions, Results.competition_id == Competitions.competition_id)
        .where(and_(Results.user_id == user.id, Results.status != status_wait_adm))
        .group_by(Results.competition_id, Competitions.title)
    )

    competition_data = []
    for row in competitions:
        competition_id, title, user_count = row
        
        # Get total participants in the competition
        members = await session.scalar(
            select(func.count(Results.user_id)).where(and_(Results.competition_id == competition_id, Results.status != status_wait_adm))
        )
        
        # Get user's place by count
        subquery = (
            select(
                Results,
                func.row_number().over(order_by=Results.count.desc()).label('row_number')
            )
            .filter(Results.competition_id == competition_id)
            .filter(Results.status != status_wait_adm)
            .subquery()
        )

        # Основной запрос
        query = select(subquery.c.row_number).filter(subquery.c.user_id == user.id)
    
        # Выполнение запроса
        result = await session.execute(query)
        user_place = result.scalar()
        
        # Get the competition end date
        end_date = await session.scalar(
            select(Competitions.end_date).where(Competitions.competition_id == competition_id)
        )
        
        competition_data.append({
            "title": title,
            "count": user_count,
            "members": members,
            "place": user_place,
            "end_date": end_date
        })
    
    return competition_data



async def get_user_result_by_competition_special_for_denied_result(session: AsyncSession, user, competition):
    stmt = select(Results).where(and_(Results.user_id == user.id, Results.competition_id == competition.competition_id))
    result = await session.execute(stmt)
    data = result.scalars().first()
    return data