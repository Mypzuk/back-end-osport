
from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Users, Results

from .dependencies import user_password_check

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
    return {"status": "Удачно", "message": "Пользователь успешно обновлен"} 


async def update_user_data(session: AsyncSession, user, user_update):

    for name, value in user_update:
        setattr(user, name, value)
    await session.commit()
    return {"status": "Удачно", "message": "Пользователь успешно обновлен"} 


async def check_user_password(session: AsyncSession, user, user_password):
    await user_password_check(user, user_password)
    return True




async def change_user_password(session: AsyncSession, user, user_password):
    user.password = user_password.password
    await session.commit()
    return {"status": "Удачно", "message": "Пароль успешно обновлен"} 





async def user_profile(session: AsyncSession, user):
    
    #     # Ваш исходный запрос
    # stmt = select(Results).where(Results.user_id == user.id)

    # # Измените запрос, чтобы он считал количество записей
    # count_stmt = select(func.count()).select_from(stmt.subquery())

    # # Выполнение запроса и получение результата
    # result = session.execute(count_stmt).scalar()
    
    result = await session.scalar(
            select(func.count(Results.competition_id)).where(Results.user_id == user.id)
        )


    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "competitions":result,
        "current_experience": user.current_experience,
        "level": int(user.total_experience / 100 )

    }

    return user_data