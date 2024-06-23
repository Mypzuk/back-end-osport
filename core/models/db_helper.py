from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import settings

class DatabaseHelper:
    
    def __init__(self, url: str, echo: bool = False, echo_pool: bool = False):
        
        self.engine = create_async_engine(
            url=url, 
            echo=echo,
            echo_pool=echo_pool
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine, 
            autoflush=False, 
            autocommit=False, 
            expire_on_commit=False
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self):
        async with self.session_factory() as session: 
            yield session 


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool
)
