from pydantic import BaseModel
from datetime import date

class Competition(BaseModel): 
    id: int


class CompetitionCreate(BaseModel):
    title: str 
    type: str
    password: str 
    coefficient: float 
    video_instruction: str 
    end_date: date


class CompetitionUpdate(CompetitionCreate):
    pass