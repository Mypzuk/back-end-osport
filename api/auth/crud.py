from fastapi import Depends, HTTPException, status
from datetime import timedelta
from .functions_auth import create_access_token, create_refresh_token, verify_token, token_config, rotate_refresh_token


async def login(user):
    access_token_expires = timedelta(
        minutes=token_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires
    )
    refresh_token = await create_refresh_token(data={"user_id": user.id})
    return {
        "user_id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def refresh_token(refresh_token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = await verify_token(refresh_token, credentials_exception)

    new_access_token = await create_access_token(data={"user_id": token_data.user_id})
    new_refresh_token = await rotate_refresh_token(refresh_token)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
