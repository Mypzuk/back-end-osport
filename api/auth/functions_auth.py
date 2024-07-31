from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

from fastapi import HTTPException, status

from .schemas import TokenData

# import secrets

# secret_key = secrets.token_urlsafe(32)
secret_key = "abcd"


class TokenConfig(BaseSettings):
    SECRET_KEY: str = Field(default=secret_key, env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=40, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=30, env="REFRESH_TOKEN_EXPIRE_DAYS")


token_config = TokenConfig()


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=token_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, token_config.SECRET_KEY, algorithm=token_config.ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=token_config.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, token_config.SECRET_KEY, algorithm=token_config.ALGORITHM)
    return encoded_jwt


async def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, token_config.SECRET_KEY,
                             algorithms=[token_config.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data


async def refresh_token(refresh_token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, token_config.SECRET_KEY, algorithms=[
                             token_config.ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    access_token_expires = timedelta(
        minutes=token_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = await create_access_token(
        data={"sub": token_data.login}, expires_delta=access_token_expires
    )
    return {"access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer"}


async def rotate_refresh_token(refresh_token: str):
    # Verify the old refresh token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, token_config.SECRET_KEY, algorithms=[
                             token_config.ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    # Create a new refresh token
    new_refresh_token = await create_refresh_token(data={"user_id": token_data.user_id})
    return new_refresh_token
