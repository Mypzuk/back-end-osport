from fastapi import UploadFile, File, APIRouter, Query
import shutil
import os

from .functions.squats import check_squats
from .functions.push_ups import check_pushUps
from .functions.climber import check_climber
from .functions.bicycle  import check_bicycle
from .functions.pull_ups import check_pull

from core import BASE_DIR

from .schemas import ItemType

router = APIRouter(tags=["Video"])

@router.post("/")
async def video(id: str, type: ItemType = Query(..., description="Choose an video type"), video: UploadFile = File(...)):
    try:
        with open(f"api/cv/cvmedia/{video.filename}", "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        if type == "pushUps":
            count = await check_pushUps(video.filename)

        if type == "squats":
            count = await check_squats(video.filename)

        if type == "climber":
            count = await check_climber(video.filename)

        if type == "bicycle":
            count = await check_bicycle(video.filename)

        if type == "pullUps":
            count = await check_pull(video.filename)

        os.remove(f"api/cv/cvmedia/{video.filename}")
        return count
    except Exception as e:
        return {"error": f"Произошла ошибка при загрузке файла: {str(e)}"}