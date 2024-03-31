from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import async_session
from db import db_user
from schemas import UserBase, UserDisplay

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/")
async def create_user(user: UserBase, session: AsyncSession = Depends(async_session)) -> UserDisplay:
    user = await db_user.create_user(
        session,
        user,
    )
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(async_session)):
    status = await db_user.delete_user(
        session,
        user_id,
    )
    return {"status": status}
