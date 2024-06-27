from pydantic import BaseModel

class Result(BaseModel):
    id: int

class ResultCreate(BaseModel):
    competition_id: int
    user_id: int
    video: str
    count: int
    points: float
    status: str

class ResultUpdate(ResultCreate):
    pass