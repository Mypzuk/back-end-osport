from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Competitions

from .schemas import Competition, CompetitionCreate, CompetitionUpdate



async def get_competitions(session: AsyncSession):
    stmt = select(Competitions).order_by(Competitions.competition_id)
    result: Result = await session.execute(stmt)
    competitions = result.scalars().all()
    return list(competitions)


async def get_competition(session: AsyncSession, **kwargs):
    query = select(Competitions)
    for key, value in kwargs.items():
        query = query.where(getattr(Competitions, key) == value)
    result = await session.execute(query)
    return result.scalars().first()




async def create_competition(session: AsyncSession, competition_in: CompetitionCreate ):
    competition = Competitions(**competition_in.model_dump())
    session.add(competition)
    await session.commit()
    await session.refresh(competition)
    return competition



async def delete_competition(session: AsyncSession, competition: Competition):
    await session.delete(competition)
    await session.commit()
    return {"status": "success", "message": "Competition deleted successfully"}    




async def competition_update(
        session: AsyncSession, 
        competition: Competition, 
        competition_update: CompetitionUpdate
):
    for name, value in competition_update.model_dump().items():
        setattr(competition, name, value)
    await session.commit()
    return competition




async def get_first_id(session: AsyncSession):
    stmt = select(Competitions).order_by(Competitions.competition_id.asc)
    result = await session.execute(stmt)
    first_id = result.scalars().first()
    return first_id
