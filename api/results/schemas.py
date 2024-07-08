from pydantic import BaseModel

class Result(BaseModel):
    id: int

class ResultUpdate(BaseModel):
    count: int




class ResultCreate(ResultUpdate):
    competition_id: int
    user_id: int
    points: float
    status: str
    video: str
