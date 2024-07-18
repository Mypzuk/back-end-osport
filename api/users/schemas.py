from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    id: int


class UserCreate(BaseModel):
    login: str
    email: str 
    password: str
    


class UserUpdateAfterCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    sex: str


class UserUpdateBirthday(BaseModel):
    birth_date: date



class UserLogin(BaseModel):
    login: str
    password: str


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    height: str 
    weight: str


class UserPassword(BaseModel):
    password: str

class NewUserPass(UserPassword):
    pass