from fastapi import UploadFile, File, APIRouter, Query, Depends
import shutil
import cv2
from starlette.responses import JSONResponse

import os


from .functions.squats import check_squats
from .functions.push_ups import check_pushUps
from .functions.climber import check_climber
from .functions.bicycle import check_bicycle
from .functions.pull_ups import check_pull

from api.users.schemas import UserLogin
from api.auth.dependencies import get_current_user


from core import BASE_DIR

from .schemas import ItemType


router = APIRouter(tags=["Video"])


@router.post("/")
async def video(id: str, type: ItemType = Query(..., description="Choose an video type"), video: UploadFile = File(...), check_auth: UserLogin = Depends(get_current_user),):
    try:
        with open(f"api/cv/cvmedia/{video.filename}", "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        data = cv2.VideoCapture(f'api/cv/cvmedia/{video.filename}')
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = data.get(cv2.CAP_PROP_FPS)

        # calculate duration of the video
        seconds = round(frames / fps)
        video_name, video_extension = os.path.splitext(video.filename)

        extensions = ['.mp4', '.mov']
        if video_extension.lower() not in extensions:
            return JSONResponse(status_code=404, content={"code":"404","message": "При загрузке видео произошла ошибка"})  
                                            # 750mb
        if seconds < 150 & video.size < 786432000 :
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
                
            return JSONResponse(status_code=200, content={"code":"200","message": f"{count}"})
        
        return JSONResponse(status_code=202, content={"code":"202","message": "Видео на проверке администратором"})
        # os.remove(f"api/cv/cvmedia/{video.filename}")
    except Exception as e:
        # return {"error": f"Произошла ошибка при загрузке файла: {str(e)}"}
        return JSONResponse(status_code=404, content={"code":"404","message": "При загрузке видео произошла ошибка"})  