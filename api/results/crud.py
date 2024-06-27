from sqlalchemy import select, and_, desc, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Results

from .schemas import Result, ResultCreate, ResultUpdate
from api.users.schemas import User

from api.competitions.schemas import Competition

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


async def create_result(session: AsyncSession, result_in: ResultCreate ):
    result = Results(**result_in.model_dump())
    session.add(result)
    await session.commit()
    await session.refresh(result)
    return result



async def update_reslut(
        session: AsyncSession, 
        result: Result, 
        result_update: ResultUpdate
):
    for name, value in result_update.model_dump().items():
        setattr(result, name, value)
    await session.commit()
    return result



async def delete_result(session: AsyncSession, result: Result):
    await session.delete(result)
    await session.commit()
    return {"status": "success", "message": "Result deleted successfully"}    



async def nulify_result(session: AsyncSession, result: Result):
    stmt = select(Results).where(Results.result_id == result.result_id)
    result_obj = await session.execute(stmt)
    result_row = result_obj.scalar_one_or_none()

    result_row.count = 0 
    result_row.points = 0

    return result_row



async def get_user_results(session: AsyncSession, user: User):
    stmt = select(Results).where(Results.user_id == user.id)
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)



async def get_user_result_by_competition(session: AsyncSession, user, competition):
    stmt = select(Results).where(and_(Results.user_id == user.id, Results.competition_id == competition.competition_id))
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)


async def get_competition_result(session: AsyncSession, competition):
    stmt = select(Results).where(Results.competition_id == competition.competition_id)
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)



async def get_competition_participants(session: AsyncSession, competition):
    stmt = select(Results.user_id).where(Results.competition_id == competition.competition_id).distinct()
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)



async def check_user_status_by_competition(session: AsyncSession, user, competition):
    stmt = select(Results.status).where(and_(Results.competition_id == competition.competition_id, Results.user_id == user.id))
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)



async def get_competition_rating(session: AsyncSession, competition):
    stmt = select(Results).where(Results.competition_id == competition.competition_id).order_by(desc(Results.count))
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)



async def get_total_rating(session: AsyncSession):
    stmt = select(Results.user_id, func.sum(Results.points)).filter(Results.status.isnot(None), Results.count > 0).group_by(Results.user_id).order_by(desc(func.sum(Results.count)))
    result: Result = await session.execute(stmt)
    print(result)
    data = result.scalars().all()
    print(data)