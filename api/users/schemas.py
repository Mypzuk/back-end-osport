from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    login: str
    email: str 
    password: str


class UserCreate(User):
    first_name: str
    last_name: str
    birth_date: date
    sex: str