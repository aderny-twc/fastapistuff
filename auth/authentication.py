from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.oauth2 import create_access_token
from db import db_user
from db.hash import Hash

from db.database import async_session

router = APIRouter(
    tags=["authentication", ]
)


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(async_session)):
    user = await db_user.get_user_by_username(session, username=request.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect pass or username"
        )
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect pass or username"
        )

    access_token = create_access_token(data={"username": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }
