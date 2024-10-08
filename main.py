from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
import uvicorn

from core.config import settings

from api import router as api_router

from core.models import db_helper, Base


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(api_router, prefix=settings.api_prefix)


if __name__ == "__main__":
    uvicorn.run("main:main_app", reload=True)


main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- поменять в проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
