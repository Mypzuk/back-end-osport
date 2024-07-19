from pydantic import BaseModel
from typing import Literal

class Result(BaseModel):
    id: int


class ResultUpdate(BaseModel):
    count: int



class ResultCreate(ResultUpdate):
    competition_id: int
    user_id: int
    points: float
    status: str = "checked_cv"
    video: str

class ResultDenied(ResultUpdate):
    competition_id: int
    user_id: int
    points: float
    status: str = "wait_adm"
    video: str