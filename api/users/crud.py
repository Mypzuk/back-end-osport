
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Users

from .schemas import User, UserCreate, UserUpdateBirthday

async def get_users(session: AsyncSession):
    stmt = select(Users).order_by(Users.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def create_user(session: AsyncSession, user_in: UserCreate):
    user = Users(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user




async def user_login():
    return 'Пользователь вошел'



async def get_user(session: AsyncSession, **kwargs):
    query = select(Users)
    for key, value in kwargs.items():
        query = query.where(getattr(Users, key) == value)
    result = await session.execute(query)

    return result.scalars().first()

# 
# async def get_user(session: AsyncSession, user_id: int | str):
#     return await session.get(Users, user_id)



async def delete_user(session: AsyncSession, user: User):
    await session.delete(user)
    await session.commit()
    return {"status": "Удачно", "message": "Пользователь успешно удален"}    


async def update_user_birthdate(session: AsyncSession, user: User,  user_update: UserUpdateBirthday ):
    user.birth_date = user_update.birth_date
    await session.commit()
    return {"status": "success", "message": "Пользователь успешно обновлен"} 