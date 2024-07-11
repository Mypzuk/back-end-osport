from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Whitelist

from api.users.crud import get_user

from .schemas import WhitelistIn, CheckWhitelist



async def get_whitelist_user(session: AsyncSession, whitelist_in: WhitelistIn):
    query = select(Whitelist).where(and_(Whitelist.competition_id == whitelist_in.competition_id, Whitelist.email == whitelist_in.email ))
    result = await session.execute(query)
    return result.scalars().first()


async def get_whitelist_users(session: AsyncSession):
    stmt = select(Whitelist).order_by(Whitelist.id)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)
    

async def create_whitelist_user(session: AsyncSession, whitelist_in: WhitelistIn):
    whitelist_user = Whitelist(**whitelist_in.model_dump())
    session.add(whitelist_user)
    await session.commit()
    await session.refresh(whitelist_user)
    return whitelist_user


async def get_whitelist_user_by_id(session: AsyncSession, whitelist_in: CheckWhitelist):
    user = await get_user(session=session, id = whitelist_in.user_id )
    query = select(Whitelist).where(and_(Whitelist.competition_id == whitelist_in.competition_id, Whitelist.email == user.email ))
    result = await session.execute(query)

    if result.scalars().first() is None: 
        return False
    return True