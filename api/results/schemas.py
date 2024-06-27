from pydantic import BaseModel

class Result(BaseModel):
    id: int

class ResultUpdate(BaseModel):
    video: str
    count: int
    points: float
    status: str



class ResultCreate(ResultUpdate):
    competition_id: int
    user_id: int

