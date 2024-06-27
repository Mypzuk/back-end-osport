from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    id: int


class UserCreate(BaseModel):
    login: str
    email: str 
    password: str
    first_name: str
    last_name: str
    birth_date: date
    sex: str


class UserUpdateBirthday(BaseModel):
    birth_date: date