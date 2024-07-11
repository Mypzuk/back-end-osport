from fastapi import APIRouter

from .users.views import router as user_router

from .competitions.views import router as competition_router

from .results.views import router as result_router

from .cv.views import router as video_router

from .whitelist.views import router as whitelist_router

router = APIRouter()

router.include_router(router=user_router, prefix="/user")
router.include_router(router=competition_router, prefix="/competition")
router.include_router(router=result_router, prefix="/result")
router.include_router(router=video_router, prefix="/video")
router.include_router(router=whitelist_router, prefix="/whitelist")